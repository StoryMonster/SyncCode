$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
python $ScriptDir\CodeSync\main.py --config-file=$ScriptDir\config.ini $args

if ($?)
{
    "Sync code successfully!"
}
else
{
    "Sync code fail!"
}