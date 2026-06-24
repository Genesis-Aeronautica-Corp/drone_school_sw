# choose shell
set windows-shell := ["powershell.exe", "-NoProfile", "-Command"]
set shell := ["bash", "-c"]

[windows]
install:
  winget install -e --id Python.Python.3.13
  pip install pyinstaller requests --break

[macos]
install:
  pip install pyinstaller requests --break  
  
[linux]
install:
  pip install pyinstaller requests --break 
  echo 'PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

[linux]
build:
  rm -rf dist build
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_x86-64_Ubuntu.sh" --console --bootloader-ignore-signals

[macos]
build:
  rm -rf dist build
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_MacOS" --console --bootloader-ignore-signals

[windows]
build:
  rm -r -fo dist\*
  rm -r -fo build\*
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_x86-64_windows.exe" --console --bootloader-ignore-signals

[linux]
run:
  dist/ClientSessStarter_x86-64_Ubuntu.sh

[macos]
run:
  dist/ClientSessStarter_MacOS

[windows]
run:
  .\dist\ClientSessStarter_x86-64_windows.exe
