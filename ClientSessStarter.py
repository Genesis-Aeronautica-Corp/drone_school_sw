import os
import json
from typing import List
from dataclasses import dataclass
import logging
import sys
from pathlib import Path

from vpn import TSManager
from utils import post_request

logger = logging.getLogger("SessStarter")

# === Constants ===
RFD_DOMAIN_NAME = "prod.rfd.genesisaero.org"
RFD_MM_URL = f"https://{RFD_DOMAIN_NAME}/missions"
RFD_URL = f"https://{RFD_DOMAIN_NAME}/connections"
RFD_CONNECT_URL = f"{RFD_URL}/get-vpn-connection"
RFD_DELETE_CONN_URL = f"{RFD_URL}/delete-vpn-connection"
RFD_AUTH_URL = f"https://{RFD_DOMAIN_NAME}/auth"

BASE_PATH = Path()

if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys.executable).parent
else:
    BASE_PATH = Path(__file__).parent


def get_missions(jwt, email) -> List | None:
    res = post_request(
        url=RFD_MM_URL + "/get-missions-list",
        payload={"email": email, "status": "in progress"},
        description=f"Get missions list for user {email}",
        jwt=jwt,
    )
    if not res:
        logger.error(f"Can't get missions list for user {email}")
        return None
    else:
        data = res["data"]
        logger.info(f"Fetched missions {data} from RFD MM")
        return data


@dataclass
class VpnConnData:
    token: str
    hostname: str
    token_hash: str


def get_vpn_connection(mission_id, jwt) -> VpnConnData | None:
    """
    Sends a request to the RFD to retrieve VPN connection credentials using RSA public key encryption.
    Expects a base64-encoded token in response, which it decrypts with the private key.
    """
    logger.info("Requesting VPN credentials from Remote Flights Dispatcher...")
    logger.info("Sending get-vpn-connection request to RFD")

    payload = {"tag": "client", "mission_id": mission_id}

    # Send request
    res = post_request(
        RFD_CONNECT_URL,
        payload,
        "Client get-vpn-connection",
        jwt=jwt,
        timeout=10,
        retries=3,
    )
    if res:
        token = res.get("token")
        hostname = res.get("hostname")
        token_hash = res.get("token_hash")

        logger.info("✅ VPN credentials obtained.")
        return VpnConnData(token=token, hostname=hostname, token_hash=token_hash)
    else:
        logger.error("❌ Can't obtain VPN credentials. Please contact admin")
        return None


def delete_vpn_connection(jwt, token_hash, hostname) -> bool:
    """
    Informs the RFD that this client's VPN credentials should be revoked.
    """
    logger.info("Deleting VPN credentials from Remote Flights Dispatcher...")

    payload = {"hostname": hostname, "token_hash": token_hash}
    res = post_request(
        RFD_DELETE_CONN_URL,
        payload,
        "Client delete-vpn-connection",
        jwt=jwt,
        timeout=10,
    )
    if res:
        logger.info("✅ VPN credentials deleted from RFD.")
    else:
        logger.info("❌ Can't delete VPN credentials from RFD. Please contact admin")

    return res is not None


def main():
    print("👋 Welcome to the Remote Flight Session Starter\n")
    email = None
    psswd = None
    if os.path.exists(BASE_PATH / "credentials.json"):
        creds = json.load(open(BASE_PATH / "credentials.json"))
        email = creds["email"]
        psswd = creds["password"]

    if not email:
        email = input("Enter email: ")
    if not psswd:
        psswd = input("Enter password: ")

    res = post_request(
        url=RFD_AUTH_URL + "/login",
        payload={"email": email, "password": psswd},
        description="Login to RFD",
    )

    if res is None:
        logger.error("Can't login to RFD")
        print("❌ Authentication failed. Check your email and password")
        return 1

    jwt = res.get("jwt")
    if jwt is None:
        logger.error("Can't decode JWT")
        return 1

    print("✅ User authentication success")

    json.dump({"email": email, "password": psswd}, open(BASE_PATH / "credentials.json", "w"))

    missions = get_missions(jwt, email)
    if missions is None:
        print("❌ Error: no active missions found")
        logger.error("Can't get missions")
        return 1

    mission_id = None
    for m in missions:
        if m["status"] == "in progress":
            mission_id = m["mission_id"]
            break
    if mission_id is None:
        print("❌ Error: no active missions found")
        logger.error("No active missions found")
        return 1

    vpn_conn = get_vpn_connection(mission_id, jwt)
    if vpn_conn is None:
        print(
            "❌ Error: can't get VPN credentials. Most likely your instructor hasn't started your session yet"
        )
        return 1

    print("⚙️ Starting Tailscale")

    tsm = TSManager(logger.info)
    if not tsm.start(vpn_conn.token, vpn_conn.hostname):
        logger.error("Can't start Tailscale")
        print("Failed to start Tailscale. Contact your instructor")
        return 1

    print("\n\n\n🌐 Tailscale started, you are ready to work")
    print("⚠️ Don't close this script until the end of yout flight session")
    print("\nℹ️ To close simply hit Enter on your keyboard\n\n")
    print(
        "🚫 You should close this window only after you've pressed Enter and the script correctly finished."
    )
    try:
        while True:
            inp = input()
            if inp == "":
                logger.info("Interrupted by user")
                break

    except KeyboardInterrupt:
        logger.info("Interrupted by user")

    if not tsm.close():
        print("❌ Failed to disconnect from Tailscale. Please do it manually")
        logger.error("Can't disconnect from Tailscale")

    if not delete_vpn_connection(jwt, vpn_conn.token_hash, vpn_conn.hostname):
        logger.error("Can't delete VPN credentials from RFD")

    print("🤝 Exiting")

    return 0


if __name__ == "__main__":
    import datetime

    LOG_PATH = BASE_PATH / "logs"
    if not os.path.exists(LOG_PATH):
        os.mkdir(LOG_PATH)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(
                LOG_PATH
                / f"ClientSessStarter_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                encoding="utf-8",
            ),
        ],
    )

    sys.exit(main())
