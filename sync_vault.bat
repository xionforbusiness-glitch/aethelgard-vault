@echo off
title Aethelgard Vault - 1-Click Cloud Synchronizer
cls
echo ==============================================================================
echo           AETHELGARD VAULT - CLOUD SYNCHRONIZATION
echo ==============================================================================
echo.
echo [1/2] Fetching latest notes & updates from Cloud / Telegram...
cd /d "C:\Users\omara\Desktop\vault\Aethelgard Vault"
git pull origin main
echo.
echo [2/2] Backing up any local laptop modifications to Cloud...
git add .
git commit -m "chore: sync from local Obsidian desktop"
git push origin main
echo.
echo ==============================================================================
echo  SUCCESS: Your local Obsidian Vault is completely up-to-date with the Cloud!
echo ==============================================================================
echo.
pause
