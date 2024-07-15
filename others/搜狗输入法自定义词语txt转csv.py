import csv

# 定义输入文件和输出文件的名称
input_file = 'input.txt'
output_file = 'output.csv'

# 读取输入文件中的数据
with open(input_file, 'r', encoding='utf-8') as file:
    data = file.readlines()

# 处理数据并保存为CSV
rows = []

for line in data:
    line = line.strip()  # 去除每行的换行符
    if line:  # 确保不是空行
        input_code, rest = line.split(',')
        position, replace_text = rest.split('=')
        rows.append([input_code, replace_text, position])

# 将处理后的数据写入CSV文件
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['输入码', '替换文本', '位置'])
    csvwriter.writerows(rows)

print(f"数据已保存到 {output_file}")
