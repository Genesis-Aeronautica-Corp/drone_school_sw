import os
import json
import logging
import uuid
import subprocess
from utils import post_request

logger = logging.getLogger("InstructorSessStarter")

# HAS TO BE REDEFINIED FOR THE HOST
INVITE_CMD = ["ros2", "run", "frontend", "efga"]

# Base URL to communicate with Remote Flights Dispatcher (RFD)
RFD_DOMAIN_NAME = "prod.rfd.genesisaero.org"
RFD_URL = f"https://{RFD_DOMAIN_NAME}/connections"
RFD_MM_URL = f"https://{RFD_DOMAIN_NAME}/missions"
RFD_START_SESS_URL = RFD_URL + "/start-session"
RFD_GCS_SESS_FINISH_URL = RFD_URL + "/close-session"

# ============================
# RFD Registration and Session
# ============================

RFD_REPORT_RETRIES = 3
RFD_GCS_REGISTER_URL = f"https://{RFD_DOMAIN_NAME}/auth/login"


def gcs_auth(email: str, password: str) -> str | None:
    """
    Authenticates the Ground Control Station (GCS) user with the Remote Flights Dispatcher (RFD).
    Saves the JWT token to a state variable.
    """
    logger.info("Sending auth/login request to RFD")

    payload = {"email": email, "password": password}
    res = post_request(
        RFD_GCS_REGISTER_URL, payload, "GCS auth with RFD", RFD_REPORT_RETRIES
    )

    jwt = None
    if res:
        jwt = res.get("jwt")
        logger.info("✅ GCS user successfully authenticated.")
    else:
        logger.error("❌ GCS user authentication failed")

    return jwt


# ============================
# Active missions list request
# ============================


def format_missions(missions: list) -> str:
    if not missions:
        return "No active missions found"

    formatted = []
    for i, mission in enumerate(missions, start=1):
        card = (
            f"=== Mission #{i} ===\n"
            f"🆔 Mission ID   : {mission.get('mission_id')}\n"
            f"👤 Email        : {mission.get('email')}\n"
            f"📦 Group        : {mission.get('mission_group')}\n"
            f"🎯 Type         : {mission.get('mission_type')}\n"
            f"📍 Location     : {mission.get('location')}\n"
            f"🚁 Drone Type   : {mission.get('drone_type')}\n"
            f"⏱️ Time Window  : {mission.get('time_window')}\n"
            f"📊 Status       : {mission.get('status')}\n"
        )
        formatted.append(card)

    return "\n".join(formatted)


def get_missions(jwt):
    try:
        logger.info("Sending get-missions-list request")
        res = post_request(
            url=RFD_MM_URL + "/get-missions-list",
            payload={
                "mission_group": "default",
                "status": "in progress",
            },
            description="Get missions list",
            jwt=jwt,
        )
        if res:
            logger.info("get-missions-list request success")
            return res.get("data")
        else:
            logger.warning("❌ Can't get missions from RFD")
    except Exception as e:
        logger.error(f"❌ Failed to get missions from RFD: {e}")

    return None


# ========= SESS LIFECYCLE ===========


def start_session(mission_id, jwt) -> str | None:
    """
    Reports the start of a new mission session to the RFD.
    Includes session ID, mission ID.
    """
    session_id = str(uuid.uuid4())
    logger.info("Sending start-session report to RFD for session")

    payload = {"mission_id": mission_id, "session_id": session_id}

    res = post_request(
        RFD_START_SESS_URL,
        payload,
        "GCS start-session",
        RFD_REPORT_RETRIES,
        jwt=jwt,
    )
    if res:
        logger.info("✅ Session start reported successfully")
        return session_id
    else:
        logger.error("❌ Session start report failed. Please contact admin")
        return None


# ----------------------------


def close_session(session_id, jwt) -> bool:
    """
    Reports the end of a session to the RFD
    """
    logger.info("Sending close-session report")

    payload = {"session_id": session_id, "result": "finish"}

    res = post_request(
        RFD_GCS_SESS_FINISH_URL,
        payload,
        "GCS close-session",
        RFD_REPORT_RETRIES,
        jwt=jwt,
    )
    if res:
        logger.info("✅ Session close report sent successfully")
    else:
        logger.error("❌ Session close report failed. Please contact admin")

    return res is not None


def main():
    if len(INVITE_CMD) == 0:
        logger.error("No invite command specified")
        return 1

    email = None
    pswd = None
    if os.path.exists("credentials.json"):
        creds = json.load(open("credentials.json"))
        email = creds["email"]
        pswd = creds["password"]

    if not email:
        email = input("Enter email: ")
    if not pswd:
        pswd = input("Enter password: ")

    json.dump({"email": email, "password": pswd}, open("credentials.json", "w"))

    jwt = gcs_auth(email, pswd)
    if not jwt:
        logger.error("Failed to authenticate in RFD")
        return 1

    logger.info("Auth success")

    missions = get_missions(jwt)
    if not missions:
        logger.error("Failed to get missions list")
        return 1

    print(format_missions(missions))

    n = int(input("Enter mission number: ")) - 1

    if n < 0 or n >= len(missions):
        logger.error(f"Invalid mission number {n}")
        return 1

    mission_id = missions[n]["mission_id"]

    session_id = start_session(mission_id, jwt)
    if not session_id:
        logger.error("Failed to start session")
        return 1

    logger.info("Session created")

    logger.info("Inviting client")

    while True:
        try:
            subprocess.run(INVITE_CMD + [f"client-{session_id[-8:]}"])
        except KeyboardInterrupt:
            r = input("Type 'restart' to restart invite service: ")
            if r != "restart":
                break

    close_session(session_id, jwt)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    )
    main()
