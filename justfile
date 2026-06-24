[linux]
build:
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_x86-64_Ubuntu" --console --bootloader-ignore-signals

[macos]
build:
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_MacOS" --console --bootloader-ignore-signals

[windows]
build:
  pyinstaller ClientSessStarter.py --onefile -n "ClientSessStarter_x86-64_windows.exe" --console --bootloader-ignore-signals

[linux]
run:
  dist/ClientSessStarter_x86-64_Ubuntu

[macos]
run:
  dist/ClientSessStarter_MacOS

[windows]
run:
  dist\ClientSessStarter_x86-64_windows.exe
