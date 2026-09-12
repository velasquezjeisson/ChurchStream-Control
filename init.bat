@echo off

REM ==========================================================
REM CHURCHSTREAM CONTROL - INICIADOR
REM ==========================================================

cd /d "%~dp0"


REM ==========================================================
REM BUSCAR OPENLP
REM ==========================================================

set "OPENLP_EXE="


REM Instalacion normal

if exist "%ProgramFiles%\OpenLP\OpenLP.exe" (

    set "OPENLP_EXE=%ProgramFiles%\OpenLP\OpenLP.exe"

)


REM Instalacion 32 bits

if not defined OPENLP_EXE (

    if exist "%ProgramFiles(x86)%\OpenLP\OpenLP.exe" (

        set "OPENLP_EXE=%ProgramFiles(x86)%\OpenLP\OpenLP.exe"

    )

)


REM Instalacion por usuario

if not defined OPENLP_EXE (

    if exist "%LocalAppData%\Programs\OpenLP\OpenLP.exe" (

        set "OPENLP_EXE=%LocalAppData%\Programs\OpenLP\OpenLP.exe"

    )

)


REM ==========================================================
REM INICIAR OPENLP
REM ==========================================================

tasklist /FI "IMAGENAME eq OpenLP.exe" 2>NUL | find /I "OpenLP.exe" >NUL

if %ERRORLEVEL% NEQ 0 (

    if defined OPENLP_EXE (

        start "" "%OPENLP_EXE%"

        timeout /t 8 /nobreak >nul

    )

)


REM ==========================================================
REM API HIMNARIO ADVENTISTA
REM ==========================================================

if exist "%~dp0himadve-api\package.json" (

    where bun >nul 2>&1

    if not errorlevel 1 (

        REM --------------------------------------------------
        REM INSTALAR DEPENDENCIAS SI ES NECESARIO
        REM --------------------------------------------------

        if not exist "%~dp0himadve-api\node_modules" (

            pushd "%~dp0himadve-api"

            bun install

            popd

        )


        REM --------------------------------------------------
        REM INICIAR API HIMNARIO
        REM --------------------------------------------------

        start "" /B cmd /c ^
        "cd /d ""%~dp0himadve-api"" && bun run start"

    )

)


REM ==========================================================
REM INICIAR CHURCHSTREAM SERVER
REM ==========================================================

where py >nul 2>&1

if %ERRORLEVEL% EQU 0 (

    start "" /B py server.py

) else (

    start "" /B python server.py

)


REM ==========================================================
REM FIN DEL INICIADOR
REM ==========================================================

exit