import os
import yaml

def update_metadata_in_directory(directory):
    # 遍历目录中的所有文件
    for index, filename in enumerate(os.listdir(directory)):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                lines = content.split('\n')

                # 寻找元数据块
                metadata_start = None
                metadata_end = None
                for i, line in enumerate(lines):
                    if line.strip() == '---':
                        if metadata_start is None:
                            metadata_start = i
                        else:
                            metadata_end = i
                            break

                if metadata_start is not None and metadata_end is not None:
                    # 解析元数据
                    metadata_content = '\n'.join(lines[metadata_start + 1:metadata_end])
                    metadata = yaml.safe_load(metadata_content)

                    # 检查是否存在cover
                    if 'cover' not in metadata:
                        # 在元数据中添加cover
                        cover_url = f'https://t.mwm.moe/fj/?{index}'
                        metadata['cover'] = cover_url

                        # 更新元数据内容
                        updated_metadata_content = yaml.dump(metadata, default_flow_style=False, allow_unicode=True)

                        # 替换原始元数据内容
                        lines[metadata_start + 1:metadata_end] = updated_metadata_content.split('\n')

                        # 重新构建文件内容
                        updated_content = '\n'.join(lines)

                        # 写回文件
                        with open(filepath, 'w', encoding='utf-8') as updated_file:
                            updated_file.write(updated_content)
                            print(f"文件 '{filename}' 元数据已更新，cover链接为: {cover_url}")
                    else:
                        print(f"文件 '{filename}' 已存在cover，无需操作")
                else:
                    print(f"文件 '{filename}' 未找到元数据块")

# 使用示例，当前目录下的所有Markdown文件
update_metadata_in_directory('.')
