@echo off
SETLOCAL

set TSD_BIN=%1
set STATE_DIR=%2

echo Stopping Tailscale service...
powershell -Command "Stop-Service Tailscale" || exit /b 1

echo Removing state...
rmdir /s /q "%STATE_DIR%" || exit /b 1

echo Starting Tailscale service again...
powershell -Command "Start-Service Tailscale" || exit /b 1

echo Start IPN (GUI app)
powershell -Command "if (-not (Get-Process -Name 'tailscale-ipn' -ErrorAction SilentlyContinue)) { Start-Process 'C:\Program Files\Tailscale\tailscale-ipn.exe'; Start-Sleep -Seconds 2 }"

echo Done
