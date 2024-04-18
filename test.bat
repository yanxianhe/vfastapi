@echo off
setlocal enabledelayedexpansion
set "env_to_use=%~1"
set "RUN_TEST=py.test TestClient.py"


if "%env_to_use%" == "" (
    echo No environment specified. Defaulting to 'dev'.
    set "env_to_use=dev"
)

REM 从指定的环境文件中读取变量值并设置为临时系统环境变量
:load_env
for /f "usebackq tokens=1,* delims==" %%A in ("%env_to_use%.env") do (
    REM 检查每一行
    set "current_line=%%A=%%B"
    if defined current_line (
        REM 移除等号及其前面的内容
        set "current_line=!current_line:*==!"
        if not defined current_line (
            continue
        )
        if not "!current_line:~0,1!"=="!" (
            set "%%A=%%B"
        )
    )
)

REM 根据参数值选择相应的环境文件 开发环境（dev) 测试环境(test) 生产环境（prod）
if "%env_to_use%"=="dev" (
    call %RUN_TEST%
) else if "%env_to_use%"=="test" (
    call %RUN_TEST%
) else if "%env_to_use%"=="prod" (
    call %RUN_TEST%
) else (
    echo Invalid environment parameter, only 'dev', 'test' or 'prod' are supported.
    exit /b 1
)

REM 使用 endlocal 结束局部环境，返回到主脚本
endlocal

exit /b 0