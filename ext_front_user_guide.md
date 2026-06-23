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

The app requires two key dependencies which prompt to install themselves during our app installation: `Gstreamer` and `Tailscale`.

While the latter will be prompted to install by our installer (so you don't need to download anything), `Gstreamer` has to be downloaded and installed manually:
1. Copy [the link](https://gstreamer.freedesktop.org/data/pkg/windows/1.28.4/msvc/gstreamer-1.0-msvc-x86_64-1.28.4.exe) to your browser's address line.
  - Alternatively visit [Gstreamer website](https://gstreamer.freedesktop.org/download/#windows) and download `MSVC x86_64 (VS 2022, Release CRT)` file.
2. Run downloaded gstreamer installer from your computer's `Downloads` folder and proceed with instructions:
  - **IMPORTANT:** When Gstreamer prompts whether to install itself for current user only or for all users - choose `Install for all users` (requires administrator privileges).
  - Almost all steps should be left with default settings (it's important to install `Gstreamer` in the default system path `C:\Program Files\gstreamer\`).
    - The only exception is that it's highly recommended to **turn ON** the following options on the `Select Additional Tasks` step:
    - `Set or update the GSTREAMER_1_0_ROOT_MSVC_X86_64 environtment variable`
    - `Set or update the GStreamer1.0 Registry variable`.

The application logs are stored in `C:\Users\<USERNAME>\AppData\Local\ExternalFrontend\`.

### MacOS (14, 15, 26)

The app is distributed via `.dmg` file which installs the app on the computer. Just install it the normal way, dragging our app to the `Applications` folder.

Besides the main app some dependencies have to be manually installed via [homebrew](https://brew.sh) package manager.
  - Open your terminal and run the command from [homebrew website](https://brew.sh):
    ```bash
    # Install developer tools
    xcode-select --install 

    # Install homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
  - After Homebrew is installed run the following command in the Terminal:
    ```bash
    brew update
    brew install qt6 gstreamer sdl2 zeromq
    ```

  - Finally, you should give our application permissions to run:
    ```bash
    sudo xattr -cr /Applications/ExternalFrontend.app
    ```

The application logs are stored in `~/Library/Application\ Support/ExternalFrontend/`.

## App usage

Currently, due to some security reasons, `External Frontend` has to be invited by the `Backend` to operate. That's why when you run the app you will see a dialog which asks you to wait. 

Backend administrator will invite you to the app and you will be able to start using it.

## Troubleshooting

- Windows app fails to launch with due to `missing .dll files` error it's most likely that you have installed Gstreamer in an incorrect way. 
  - Go to `Launch menu` -> `Add or remove programs`
  - Uninstall Gstreamer there
  - Then run our installer again and follow the above instructions for Windows precisely, especially make sure you install it for all users.

- MacOS application fails to run and tells that the app is broken or corrupted. 
  - Most likely you haven't give it permissions. 
  - Run `sudo xattr -cr /Applications/ExternalFrontend.app`. 
  - If the file is missing, go to our `.dmg`, run it again and make sure you drag the icon of our app into the `Applications` folder.

- MacOS appication fails to run silently without any feedback.
  - Make sure you have installed all the necessary dependencies via `homebrew`.
