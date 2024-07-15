import pandas as pd
from datetime import datetime
import os

# 读取Excel表格
excel_path = "统计结果.xlsx"  # Excel文件名
df = pd.read_excel(excel_path)

# 按课程名字和任课老师分组
grouped_by_course_teacher = df.groupby(["课程名字", "任课老师"])

# 读取已有的Markdown数据
markdown_file_path = "数据提取.md"  # Markdown文件名
try:
    with open(markdown_file_path, "r", encoding="utf-8") as existing_file:
        existing_data = existing_file.read()
except FileNotFoundError:
    existing_data = ""

# 生成更新日志和数据汇总
update_log = f'# 更新日志 {datetime.now().strftime("%Y-%m-%d")}\n\n'
data_summary = "# 数据汇总\n\n"

data_summary = "约十分钟后刷新生效\n\n"

for (course_name, teacher), group in grouped_by_course_teacher:
    # 数据汇总
    data_summary += f'{course_name} - {teacher} - {group["年份"].iloc[0]} - {group["校区"].iloc[0]}\n'

# 保存数据汇总到新文件（覆盖源文件）
summary_file_path = "汇总信息.md"
with open(summary_file_path, "w", encoding="utf-8") as summary_file:
    summary_file.write(update_log + data_summary)


print(f"数据汇总已保存到 {summary_file_path}")

# 遍历每个课程和老师的分组
for (course_name, teacher), group in grouped_by_course_teacher:
    # 遍历每一行数据
    for index, row in group.iterrows():
        reason = row["理由"]
        year = row["年份"]
        course_id = row["ID"]

        # 将数据格式化为Markdown形式
        markdown_data = f"## {course_name}\n"
        # 校区判断，生成相应的隐藏标签
        campus_tag = ""
        if row["校区"] == "曲阜":
            campus_tag = "{% hideToggle 曲阜 , #FAF0E6 , #000000%}\n"
        elif row["校区"] == "日照":
            campus_tag = "{% hideToggle 日照 , #FAF0E6 , #000000%}\n"
        markdown_data = markdown_data + campus_tag
        markdown_data += f"### {teacher}\n"
        markdown_data += f"{reason}\n"
        markdown_data += f">{course_id}{year}\n\n"
        markdown_data += "{% endhideToggle %}\n"

        # 如果已有该课程和老师的数据，追加在已有数据后面
        if f"### {course_name}\n#### {teacher}\n" in existing_data:
            existing_data = existing_data.replace(
                f"### {course_name}\n#### {teacher}\n",
                f"### {course_name}\n#### {teacher}\n{reason}\n>{course_id}{year}\n\n"
                + campus_tag,
            )
        else:
            existing_data += markdown_data

        # 回显每个课程和老师数据处理完成的消息
        print(f"{course_name} - {teacher} 的数据已处理完成")

# 保存到Markdown文件中（覆盖源文件）
markdown_file_path = "数据提取.md"
with open(markdown_file_path, "w", encoding="utf-8") as file:
    file.write(existing_data)


print(f"Markdown数据已更新到 {markdown_file_path}")

# 打开Markdown文件
os.system(markdown_file_path)

# # 等待用户输入，防止程序立即退出
# input("按Enter键退出...")
