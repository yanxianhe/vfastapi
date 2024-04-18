#!/usr/bin/env sh

set -e

# 加载环境变量的函数，增加了对文件格式的 basic 检查
load_env() {
    if [ ! -f "${1}.env" ]; then
        echo "File ${1}.env not found"
        exit 1
    fi

    # 从文件中读取每一行，并增加对格式的简单验证
    while read line; do
        # 跳过空行和注释行

        key="${line%%=*}"
        value="${line#*=}"
        if [ -z "$key" ] || expr "$key" : '.*#' >/dev/null; then
            continue
        fi
        # 检查等号两侧是否为空
        if [ -z "$key" ] || [ -z "$value" ]; then
            echo "Invalid environment variable format: $line"
        else
            # 设置环境变量
            export "$key"="$value"
        fi
    done < "${1}.env"
}

# 启动 UVicorn 的函数，增加了错误捕获
start_test_uvicorn() {
    echo "Executing ${1} configuration script..."
    load_env "$1" || true
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
}

# 检查参数个数
if [ $# -eq 0 ]; then
    echo "No environment specified. Defaulting to 'dev'."
    env_to_use="dev"
else
    env_to_use="$1"
fi

# 使用 case 语句来处理特定的环境启动
case "$env_to_use" in
    dev|test|prod)
        start_test_uvicorn "$env_to_use"
        ;;
    *)
        echo "Unknown environment: $1"
        echo "Available environments: dev, test, prod"
        exit 1
        ;;
esac

# 检查命令执行的返回值，确保脚本的健壮性
if [ $? -ne 0 ]; then
    echo "Failed to start the application in the specified environment."
    exit 1
fi
