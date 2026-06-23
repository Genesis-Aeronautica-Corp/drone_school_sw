# External Frontend User Guide

`External Frontend` is a standalone cross-platform application which allows to use the Platform without complicated and Linux-centered infrastructure.

## Install

This section describes how to start using the `External Frontend` on your computer for three currently supported OS.

### Ubuntu (24.04, 26.04)

The app is distributed in a form of `.tar.gz` archive with `install.sh` script and main executable file inside.

1. Unpack archive by double-clicking with your mouse on it.
  - Alternatively use command line:
    ```bash
    tar -zxf ExternalFrontend*tar.gz
    ```

2. Go inside the directory using the `Files` application, right-click on `install.sh` and select `Run`. This will install the necessary libraries.
  - CLI:
    ```bash
    cd ExternalFrontend*
    ./install.sh
    ```

3. Run executable by right-clicking on `ExternalFrontend_<VERSION>.AppImage`.
  - CLI:
    ```bash
    ./ExternalFrontend*
    ```

The application logs are stored in `~/.local/share/ExternalFrontend/`.

### Windows 11

The app is distributed in a form of `.exe` file which installs the app on the computer.

- The app requires two key dependencies which prompt to install themselves during our app installation: `Gstreamer` and `Tailscale`.
- Proceed with default installation of both of them (it's very important to install them in the default system paths).
  - The only exception is that it's highly recommended to **turn ON** the following options on the `Select Additional Tasks` step:
    - `Set or update the GSTREAMER_1_0_ROOT_MSVC_X86_64 environtment variable`
    - `Set or update the GStreamer1.0 Registry variable`.

### MacOS (15, 26)

The app is distributed via `.dmg` file which installs the app on the computer. Just install it the normal way.

Besides the main app some dependencies have to be manually installed via [homebrew](https://brew.sh) package manager.
  - Open your terminal and run the command from [homebrew website](https://brew.sh):
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - After Homebrew is installed run the following command in the Terminal:
    ```bash
    brew install qt6 gstreamer sdl2 zeromq
    ```

## App usage

Currently, due to some security reasons, `External Frontend` has to be invited by the `Backend` to operate. That's why when you run the app you will see a dialog which asks you to wait. 

Backend administrator will invite you to the app and you will be able to start using it.
