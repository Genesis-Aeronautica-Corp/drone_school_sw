# External Frontend User Guide

`External Frontend` is a standalone cross-platform application which allows to use the Platform without complicated and Linux-centered infrastructure.

## Install

This section describes how to start using the `External Frontend` on your computer for three currently supported OS.

**Note on OS version support:**
> The version listed first (without parentheses)
> is officially supported and recommended. Versions in parentheses
> are expected to work but receive no official support guarantees.

### Windows 11 (10)

The app is distributed in a form of `.exe` file which installs the app on the computer.

The installer will prompt to install `Tailscale`, please do it since it's required for remote connectivity.

**Note:** First launch of the app can take quite a while (up to a minute) because of initialization. Next launches will be fast.

The application logs are stored in `C:\Users\<USERNAME>\AppData\Local\ExternalFrontend\`.

### MacOS 26 (15, 14)

The app is distributed via `.dmg` file which installs the app on the computer. Just install it the normal way, dragging our app to the `Applications` folder.

You should also give our application permissions to run itself. Just open the `Terminal` and execute command:

  ```bash
  sudo xattr -cr /Applications/ExternalFrontend.app
  ```

**IMPORTANT:** On the first launch you will be prompted to install `Tailscale` - the VPN client required for remote connectivity. Please give it all permissions it requests, it's critical for application's correct functioning.

- You don't have to log into any Tailscale account. Just close their app once it's been installed.
- If you already have `Tailscale` installed, the promt will not appear.
- If your existing installation is `Homebrew CLI` version of `Tailscale` (not cask), please run the command to let `Tailscale` start without `sudo`:

    ```bash
    sudo tailscale set --operator=$USER
    ```

The application logs are stored in `~/Library/Application\ Support/ExternalFrontend/`.

### Ubuntu 26.04

The app is distributed in a form of `.tar.gz` archive with `install.sh` script and main executable file inside.

1. Unpack archive by double-clicking on it with the mouse.
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

## App usage

After launching the app you will see a wizard which guides you through the `Backend` connection process.

1. On the starting screen you can either:
    - Choose to proceed without `Backend` connection (for example, if you just want to use Mission Planner).
    - Login into `Genesis Aeronautica Tailnet` using your email and password. It works only if your instructor has invited you before.
    - Proceed without login and specify `Backend`'s connection address manually.
2. On the second screen you have the following options:
    - Once again to proceed without `Backend` connection.
    - If you have logged into `Genesis Aeronautica Tailnet` (or you have your own `Tailnet` active) you can use `Scan Tailnet` button to automatically discover the `Backend`.
    - Connect to `Backend` using the discovered or manually specified address.
      - `Connect` button will connect you to the `Backend` and launch the main window of the app.

## Troubleshooting

- MacOS application fails to run and tells that the app is broken or corrupted.
  - Most likely you haven't give it permissions.
  - Run `sudo xattr -cr /Applications/ExternalFrontend.app`.
  - If the file is missing, go to our `.dmg`, run it again and make sure you drag the icon of our app into the `Applications` folder.

- MacOS or Linux application hangs during the log-in process.
  - Most likely you didn't disable `sudo` for `Tailscale` operation. Run the command:

    ```bash
    sudo tailscale set --operator=$USER
    ```
