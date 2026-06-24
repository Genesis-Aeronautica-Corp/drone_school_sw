# Software kit for Remote Drone School

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

#### System Requirements:

- 8 Gb RAM
- Intel Core i3 / Ryzen 3 CPU
- Stable Internet connection (the best option is via Ethernet cable)
- Supported OS:
  - Windows 11
  - Ubuntu 24.04 / 26.04
  - MacOS 14 / 15 / 26

#### Download and install

1. Go to [Releases](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/releases), click on the "Assets" button of the latest release and download a package for your OS.
2. Unzip the archive (usually just by double-clicking on it in your file manager or selecting "unzip" option on right-click menu) and navigate to the resulting folder.
3. There you will find two files: `ClientSessStarter` and `External Frontend` installer.
  - The first one is responsible for putting your computer into our Tailscale network.
    - It can be launched just by double-clicking on it. 
      - Please be aware that **MacOS** will probably reject the launch since we didn't managed yet to make ourself an Apple Developer account for nice and smooth software distribution (anyway MacOS is not our Tier 1 platform).
      - If your archive was downloaded into the normal `Downloads` directory, the command `xattr -cr ~/Downloads/RDS_Kit_*/ClientSessStarter*` will fix it.
      - Contact your instructor if you have any questions or problems.
  - The second one is the main application where you will work.
4. Install `External Frontend` by carefully following the [instructions](https://github.com/Genesis-Aeronautica-Corp/drone_school_sw/blob/main/ext_front_user_guide.md).
  - The installation process is not completely trivial, so do it slowly and do exactly what the instructions tell you. In case of any doubts or problems **contact your instructor**.

### Instructor

If you are reading this, we assume that our technical team has already prepared a Ubuntu machine for you.

### Developer

Repository is quite simple and straightforward. Main operations can be performed via just command (install `just` via your package manager if you don't have it already):

- `just install` -- install dependencies, necessary for this project.
- `just build` -- build `ClientSessStarter` executable for distribution.
- `just run` -- run built executable.
- `python3 InstructorSessStarter.py` -- runs the instructor's script.

## How to use

### Student

1. Wait until your instructor prepares a session for you and lets you know about it via your communication channel (ex. Telegram or Whatsapp).
2. Open `ClientSessStarter` file by double-clicking on it.
3. Enter your email and password from the account (should have been sent to you by your instructor).
4. On some systems it may require enter your password in order to get into our Tailscale VPN. Please provide it.
3. If everything is ok, you should see a message that you have been connected to Tailscale. Leave this window unclosed, it has to be running during your whole flight session.
    - If you accidentally closed it, just restart it again, no problem.
    - In case of any problems, always contact your instructor, don't try to resolve them yourself.
4. Launch `External Frontend` and wait until it will be connected to the instructor's instance.
5. Once connected, a windows with the map, log console and other things will be displayed. That's it, you can work now.
    - External Frontend is designed in a way that it can be safely closed and reopened in case of any problems. Feel free to do it, but please report all the problems to your instructor for we could resolve them in the future.

### Instructor

Assuming the hardware part (drones, radio etc) was already set up.

You will need two applications which should have been set up by our tech team on the Desktop of the working machine:
  - `InstructorSessStarter`
  - `Milocus`

1. Open `Milocus` and set up a vehicle for the student.
2. Once the student is ready, start the session by opening `InstructorSessStarter` 
3. You might be prompted with email and password for the ground teams corporate account, if so - enter it.
4. Choose a mission you are going to serve.
5. Contact the student and tell him to start the session on his side by running `ClientSessStarter`.
6. Wait until everything connects (it may take some time depending on connection quality).

## Source code

This repository contains only python scripts for establishing communication between the student and the instructor. If you need the source code of `External Frontend` please contact your instructor.
