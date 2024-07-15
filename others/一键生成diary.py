import os
import subprocess
from datetime import datetime


def generate_or_open_diary_entry():
    # 获取当前日期
    current_date = datetime.now()
    year = str(current_date.year)
    month = str(current_date.month).zfill(2)
    day = str(current_date.day).zfill(2)

    # 构建文件名和标题
    file_name = f"{year}年{month}月{day}日.md"
    title = f"{year}年{month}月{day}日"

    # 确定写入目录
    diary_dir = os.path.join(os.getcwd(), "diary")
    if not os.path.exists(diary_dir):
        os.makedirs(diary_dir)

    # 构建文件路径
    file_path = os.path.join(diary_dir, file_name)

    # 如果文件已存在，则直接打开
    if os.path.exists(file_path):
        open_file(file_path)
    else:
        # 写入元数据和标题
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"---\n")
            f.write(f"时间: {year}年{month}月{day}日\n")
            f.write(f"标题: {title}\n")
            f.write(f"---\n\n")

            # 在文件中插入标题
            f.write(f"# {title}\n\n")

        print(f"生成了日记文件: {file_path}")
        open_file(file_path)


def open_file(file_path):
    # 使用默认的文本编辑器打开Markdown文件
    if os.name == "nt":  # 检查操作系统是否为Windows
        subprocess.call(["start", "", file_path], shell=True)
    else:
        subprocess.call(["xdg-open", file_path])  # 其他操作系统可以使用xdg-open打开文件


if __name__ == "__main__":
    generate_or_open_diary_entry()
