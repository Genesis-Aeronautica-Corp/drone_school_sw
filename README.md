# Software kit for Remote Drone School

- [На русском](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/README_RU.md)
- [En español](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/README_ES.md)

## Table of contents

1. [Getting Started](#getting-started)
    - [Student](#student)
    - [Instructor](#instructor)
    - [Developer](#developer)
2. [How to use](#how-to-use)
    - [Student](#student)
    - [Instructor](#instructor)
3. [Source code](#source-code)

## Getting Started

### Student

#### System Requirements

- 8 Gb RAM
- 1 Gb of free Disk Space
- Intel Core i3 / Ryzen 3 CPU
- Stable Internet connection (the best option is via Ethernet cable)
- Supported OS versions (those in braces don't have official support but are expected to work):
  - Windows 11 (10)
  - Ubuntu 26.04 (24.04)
  - MacOS 26 (15, 14)

#### Download and install

1. Go to [Releases](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/releases), click on the "Assets" button of the latest release and download an `External Frontend` application installer for your OS.
2. Install `External Frontend` by carefully following the [instructions](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/ext_front_user_guide.md).

### Instructor

If you are reading this, we assume that our technical team has already prepared Ubuntu machine for you.

## How to use

### Student

1. Wait until your instructor prepares a session for you and lets you know about it via your communication channel (ex. Telegram or Whatsapp).
2. Open `External Frontend` application.
3. Enter your email and password on the `Login to Genesis Aeronautica Network` screen (should have been sent to you by your instructor).
4. If everything is ok, you will see `Connect to Backend` screen.
    - If there are no `Backend` URLs available, contact your Instructor. Most likely, he hasn't started his program yet.
5. Click `Connect`.
6. You will see the main window of the app. The Instructor will tell you what to do next.

### Instructor

Assuming the hardware part (drones, radio etc) was already set up.

You will need two applications which should have been set up by our tech team on the Desktop of the working machine:

- `Milocus`
- `Invite2Milocus`

1. Open `Milocus` and set up a vehicle for the student.
2. Once the student is ready, start the session by opening `Invite2Milocus`.
3. You might be prompted with email and password for the ground teams corporate account, if so - enter it.
4. Choose a mission you are going to serve.
5. Contact the student and tell him to launch `External Frontend` application and follow the instructions above.
6. Wait until everything connects (it may take some time depending on connection quality).

## Source code

This repository contains no source code and acts only as a hosting for guides and assets.
