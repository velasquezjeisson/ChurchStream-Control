@echo off
title ChurchStream Control

REM ==========================================================
REM CHURCHSTREAM CONTROL - INICIADOR
REM ==========================================================

cd /d "%~dp0"

echo.
echo ==========================================================
echo              CHURCHSTREAM CONTROL
echo ==========================================================
echo.

REM ----------------------------------------------------------
REM BUSCAR OPENLP
REM ----------------------------------------------------------

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

REM ----------------------------------------------------------
REM VERIFICAR SI OPENLP YA ESTA EJECUTANDOSE
REM ----------------------------------------------------------

tasklist /FI "IMAGENAME eq OpenLP.exe" 2>NUL | find /I "OpenLP.exe" >NUL

if %ERRORLEVEL% NEQ 0 (

    if defined OPENLP_EXE (

        echo Iniciando OpenLP...
        start "" /min "%OPENLP_EXE%"

        echo Esperando a que OpenLP inicie...
        timeout /t 8 /nobreak >nul

    ) else (

        echo.
        echo [ADVERTENCIA] No se encontro OpenLP automaticamente.
        echo ChurchStream iniciara, pero la funcion Biblia no estara disponible.
        echo.

    )

) else (

    echo OpenLP ya se encuentra ejecutandose.

)

REM ----------------------------------------------------------
REM API DEL HIMNARIO ADVENTISTA
REM ----------------------------------------------------------

echo.
echo ==========================================
echo HIMNARIO ADVENTISTA API
echo ==========================================


if not exist "%~dp0himadve-api\package.json" (

    echo [ERROR] No se encontro la carpeta himadve-api.

) else (

    where bun >nul 2>&1

    if errorlevel 1 (

        echo [ERROR] Bun no esta instalado o no esta disponible en PATH.

    ) else (

        echo Bun encontrado.


        if not exist "%~dp0himadve-api\node_modules" (

            echo Instalando dependencias del Himnario...

            pushd "%~dp0himadve-api"

            bun install

            popd

        )


        echo Iniciando API del Himnario...


        start "Himnario Adventista API" /min cmd /c ^
        "cd /d ""%~dp0himadve-api"" && bun run start"

    )

)

REM ----------------------------------------------------------
REM INICIAR SERVIDOR CHURCHSTREAM
REM ----------------------------------------------------------

echo.
echo Iniciando servidor ChurchStream...
echo.

where py >nul 2>nul

if %ERRORLEVEL% EQU 0 (
    py server.py
) else (
    python server.py
)

pause