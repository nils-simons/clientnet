@echo off
pyinstaller --onefile ..\client\client.py
RMDIR /S /Q build
del client.spec
echo Client Build Finished!
echo Starting Compling restart script...
copy ..\client\restart.au3 restart.au3
au3_x32_compiler.exe /In restart.au3
move restart.exe dist
del restart.au3
echo Restart script Build Finished!
PAUSE