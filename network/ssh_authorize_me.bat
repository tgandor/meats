@echo off

:: translated from ssh_authorize_me.sh

if [%1]==[] (
    echo "Usage: %0 user@host [-p port etc.]"
    echo "Adds id_rsa.pub (generates if missing) to user's .ssh/authorized_keys"
    goto:eof
)

ssh -o PasswordAuthentication=no %* pwd
if ERRORLEVEL 1 goto :unauthorized
echo "You are already authorized!"
goto:eof

:unauthorized
if not exist %USERPROFILE%\.ssh\id_rsa (
    echo "Generating Keys, press enter a couple of times..."
    ssh-keygen
)


type %USERPROFILE%\.ssh\id_rsa.pub | ssh %* "mkdir -p .ssh ; tee -a .ssh/authorized_keys"

ssh -o PasswordAuthentication=no %* pwd
if ERRORLEVEL 1 goto :still_unauthorized
echo "Success!"
goto:eof

:still_unauthorized
echo "Something doesn't work. Change mode to 0600 on server?"
exit /b 1
