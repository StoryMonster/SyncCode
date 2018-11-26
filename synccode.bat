@set script_path=%~dp0
@echo %script_path%
@python %script_path%\CodeSync\main.py --config-file=%script_path%\config.ini
IF %errorlevel% != 0 (
    pause
)
