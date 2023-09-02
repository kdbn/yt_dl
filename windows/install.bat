@echo off
python -m pip install --upgrade pip
python -m pip install -r %~dp0..\requirements.txt --upgrade

set icon=%~dp0youtube.ico
set command=%~dp0context.bat
set folder=explorer %~dp0..

REM Registry pathes
set contextpath=HKEY_CLASSES_ROOT\Directory\Background\shell\yt_dl
set storepath=HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\Shell

set res=4320 2160 1440 1080 720 480 360 240 144

reg add %storepath%\yt_dl_folder /f /ve /d "Config folder"
reg add %storepath%\yt_dl_folder /f /v "CommandFlags" /t REG_DWORD /d 32
reg add %storepath%\yt_dl_folder\command /f /ve /d "%folder%"

reg add %storepath%\yt_dl_default /f /ve /d "Default"
reg add %storepath%\yt_dl_default /f /v "CommandFlags" /t REG_DWORD /d 64
reg add %storepath%\yt_dl_default\command /f /ve /d "%command%"

for %%i in (%res%) do (
    set "exepath=%command% -r %%~ni"
    set "label=%%~nip"

    if %%i==1080 (set "label=%%~nip (HD)")
    if %%i==1440 (set "label=%%~nip (2K)")
    if %%i==2160 (set "label=%%~nip (4K)")
    if %%i==4320 (set "label=%%~nip (8K)")

    setlocal EnableDelayedExpansion

    reg add %storepath%\yt_dl_%%i /f /ve /d "!label!"
    reg add %storepath%\yt_dl_%%i\command /f /ve /d "!exepath!"
    endlocal
)

reg add %contextpath% /f /v Icon /d %icon%
reg add %contextpath% /f /v MUIVerb /d "Download YT here"
reg add %contextpath% /f /v SubCommands /d "yt_dl_default; yt_dl_4320; yt_dl_2160; yt_dl_1440; yt_dl_1080; yt_dl_720; yt_dl_480; yt_dl_360; yt_dl_240; yt_dl_144; yt_dl_folder"

pause
