#!/bin/bash

# 颜色定义
GREEN='\033[32m'
YELLOW='\033[33m'
RESET='\033[0m'

# 输出提示信息
printf "${GREEN}INFO ${RESET} 正在初始化，请坐和放宽...\n"

# 创建 Hexo 目录并进入
mkdir Hexo
cd Hexo

# 输出提示信息
printf "${GREEN}INFO ${RESET} 将进行 git-clone 操作\n"
printf "${GREEN}INFO ${RESET} 如果连接失败，请确认您是否可以克隆 GitHub 仓库\n"


# 初始化 Hexo
hexo init

# 安装依赖
npm install --save
npm install hexo-deployer-git --save

# 输出提示信息
printf "${GREEN}INFO ${RESET} 请查看您当前的 Hexo 版本...\n"

# 显示 Hexo 版本信息
hexo version

# 输出提示信息
printf "${GREEN}INFO ${RESET} 安装完成，您可以开始您的 Hexo 之旅了！\n"

# 提示用户停顿
printf "${GREEN}INFO ${RESET} ${YELLOW}请静待，确认无误后按 Enter 键退出！\n"

# 等待用户按下 Enter 键
read -r
