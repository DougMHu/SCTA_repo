@echo off
IF "%PYTHONPATH%" == "" GOTO NOPATH
:YESPATH
set PYTHONPATH_OLD=%PYTHONPATH%
set PYTHONPATH=C:\Users\labuser\Documents\SCTA_repo\src;%PATH%
GOTO END
:NOPATH
set PYTHONPATH=C:\Users\labuser\Documents\SCTA_repo\src;
GOTO END
:END