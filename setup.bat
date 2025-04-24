@echo off
setlocal EnableDelayedExpansion

:: Main functions
call :init
call :check_requirements || exit /b 1
call :setup_environment || exit /b 1
call :update_server_config || exit /b 1
call :display_mcp_config
pause
exit /b 0

:: Initialize variables and display header
:init
echo Domain Checker MCP Setup
echo =====================
echo.

set "CURRENT_DIR=%CD%"
echo Current directory: %CURRENT_DIR%
echo.

echo Installation Directory
echo ====================
echo Default: %CURRENT_DIR%
echo.
set /p "TARGET_DIR=Where would you like to install? (Press Enter for default): "
if "!TARGET_DIR!"=="" set "TARGET_DIR=%CURRENT_DIR%"
echo.
exit /b 0

:: Check Python installation and version
:check_requirements
echo Checking requirements...
python --version >nul 2>&1 || (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)
echo √ Python is installed

for /f "tokens=2" %%I in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%I"
echo Python version: %PYTHON_VERSION%
exit /b 0

:: Setup virtual environment and install requirements
:setup_environment
echo.
echo Creating virtual environment...
python -m venv venv || (
    echo ERROR: Failed to create virtual environment
    exit /b 1
)
echo √ Virtual environment created

echo.
echo Installing requirements...
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    call venv\Scripts\deactivate.bat
    exit /b 1
)
call venv\Scripts\deactivate.bat
echo √ Requirements installed
exit /b 0

:: Update server configuration file
:update_server_config
echo.
echo Updating server configuration...
(
echo @echo off
echo setlocal
echo.
echo set "BASEDIR=%TARGET_DIR:\=\\%"
echo.
echo REM Check and activate venv
echo if not exist "%%BASEDIR%%\venv\Scripts\activate.bat" ^(
echo     echo ERROR: Virtual environment not found. Please run setup_mcp_env.bat first.
echo     exit /b 1
echo ^)
echo.
echo call "%%BASEDIR%%\venv\Scripts\activate.bat" ^|^| ^(
echo     echo ERROR: Failed to activate virtual environment.
echo     exit /b 1
echo ^)
echo.
echo REM Run the Python script
echo python "%%BASEDIR%%\simple-domain-checker-server.py"
echo set "EXIT_CODE=%%ERRORLEVEL%%"
echo.
echo call "%%BASEDIR%%\venv\Scripts\deactivate.bat"
echo exit /b %%EXIT_CODE%%
) > domain-checker-server.bat
echo √ Server configuration updated
exit /b 0

:: Display MCP configuration
:display_mcp_config
echo.
echo Recommended MCP Configuration:
echo ============================
echo {
echo   "mcpServers": {
echo     "domain-checker": {
echo       "command": "cmd",
echo       "args": [
echo         "/c",
echo         "%TARGET_DIR:\=\\%\\domain-checker-server.bat"
echo       ],
echo       "cwd": "%TARGET_DIR:\=\\%"
echo     }
echo   }
echo }
echo.
echo Setup complete! You can now add this configuration to your Claude Desktop settings.
echo.
exit /b 0 