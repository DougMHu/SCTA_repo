@ECHO OFF

REM Command file for SCTA Unit Tests

set TESTRUN=nosetests
set DEBUGOPTS=-v -x
set LOGFILTER=--logging-filter=SCTA_repo.src.unittests
set PROGRESSOPTS=-v
set TESTDIR=unittests
set PROGRESSDIR=unittests\test-progress

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  SFU_Test              to run through all SFU unittests in debug mode
	echo.  SFU_Progress          write all SFU unittests results to a progress log
	echo.  System_Test           to run through all System unittests in debug mode
	echo.  System_Progress       write all System unittests results to a progress log
	echo.  DataLogging_Test      to run through all DataLogging unittests in debug mode
	echo.  DataLogging_Progress  write all DataLogging unittests results to a progress log
	echo.  SFU_Test              to run through all SFU unittests in debug mode
	echo.  SFU_Progress          write all SFU unittests results to a progress log
	echo.  BTC_Test              to run through all BTC unittests in debug mode
	echo.  FSW_Test              to run through all FSW unittests in debug mode
	echo.  FSW_Progress          write all FSW unittests results to a progress log
	echo.  Fastbit_Test          to run through all Fastbit unittests in debug mode
	echo.  Fastbit_Progress      write all Fastbit unittests results to a progress log
	echo.  Fireberd_Test         to run through all Fireberd unittests in debug mode
	echo.  Fireberd_Progress     write all Fireberd unittests results to a progress log
	echo.  SLG_Test              to run through all SLG unittests in debug mode
	echo.  SLG_Progress          write all SLG unittests results to a progress log
	echo.  AIM_Test              to run through all AIM unittests in debug mode
	echo.  VTM_Test              to run through all VTM unittests in debug mode
	echo.  VTM_Progress          write all VTM unittests results to a progress log
	goto end
)

if "%1" == "System_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.System %TESTDIR%\System_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "System_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\System_Test.py 2> %PROGRESSDIR%\System_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "DataLogging_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.DataLogging %TESTDIR%\DataLogging_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "DataLogging_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\DataLogging_Test.py 2> %PROGRESSDIR%\DataLogging_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "SFU_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\SFU_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "SFU_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\SFU_Test.py 2> %PROGRESSDIR%\SFU_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "BTC_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\BTC_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "BTC_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\BTC_Test.py 2> %PROGRESSDIR%\BTC_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "FSW_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\FSW_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "FSW_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\FSW_Test.py 2> %PROGRESSDIR%\FSW_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "Fastbit_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\Fastbit_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "Fastbit_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\Fastbit_Test.py 2> %PROGRESSDIR%\Fastbit_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "Fireberd_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\Fireberd_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "Fireberd_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\Fireberd_Test.py 2> %PROGRESSDIR%\Fireberd_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "SLG_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\SLG_Test.py:SLG_Test.test_loadConfigFile
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "SLG_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\SLG_Test.py 2> %PROGRESSDIR%\SLG_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

if "%1" == "AIM_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\AIM_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)
if "%1" == "VTM_Test" (
	%TESTRUN% %DEBUGOPTS% %LOGFILTER%,SCTA.Instrumentation %TESTDIR%\VTM_Test.py
	if errorlevel 1 exit /b 1
	echo.
	echo.Test Finished.
	goto end
)

if "%1" == "VTM_Progress" (
	%TESTRUN% %PROGRESSOPTS% %TESTDIR%\VTM_Test.py 2> %PROGRESSDIR%\VTM_Test-log.txt
	if errorlevel 1 exit /b 1
	echo.
	echo.Progress log written.
	goto end
)

:end
