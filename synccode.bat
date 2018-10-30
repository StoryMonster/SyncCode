@set script_path=%~dp0
@echo %script_path%
@python CodeSync\main.py --config-file=%script_path%\config.ini