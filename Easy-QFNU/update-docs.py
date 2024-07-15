import re
import datetime
import os
import requests

# 常量
modification_date_pattern = r':material-clock-edit-outline:{ title="修改日期" } (\d{4}-\d{2}-\d{2})'
creation_date_pattern = r':material-clock-plus-outline:{ title="创建日期" } (\d{4}-\d{2}-\d{2})'

# 从代码库中获取文件的创建和更新时间
def get_github_file_info(repo_owner, repo_name, file_path, github_token):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file_path}"
    headers = {"Authorization": f"token {github_token}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        commits = response.json()
        if commits:
            create_time = datetime.datetime.fromisoformat(
                commits[-1]["commit"]["committer"]["date"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d")
            update_time = datetime.datetime.fromisoformat(
                commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d")
            return create_time, update_time
        else:
            print("未找到文件的提交记录：", file_path)
    else:
        print(f"错误：{response.status_code} - {response.text}")
    return None, None

# 从文档目录中获取文件的相对路径
def get_relative_path_from_docs(file_path):
    return "docs/" + file_path.split("docs/", 1)[-1] if "docs/" in file_path else None

# 更新 Markdown 文件的日期信息
def update_markdown_files(dir_path, exclude_paths, repo_owner, repo_name, github_token):
    for root, dirs, files in os.walk(dir_path):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_paths]
        for file in files:
            file_path = os.path.join(root, file)

            # 排除不需要更新的文件
            if file_path in exclude_paths or not file.endswith(".md"):
                print(f"跳过排除的文件：{file_path}")
                continue

            file_path = file_path.replace("\\", "/")  # 统一路径分隔符为 /
            relative_path = get_relative_path_from_docs(file_path) # 获取文件相对于文档目录的路径
            if relative_path is None:
                print(f"跳过非文档文件：{file_path}")
                continue
            
            create_time, update_time = get_github_file_info(
                repo_owner, repo_name, relative_path, github_token
            )
            print("-----------------------------------------------------------")
            print(f"正在处理文件：{relative_path}\n")
            print(f"创建日期：{create_time}，更新日期：{update_time}\n")

            # 从代码库中获取 Markdown 文件的日期信息
            if create_time is None or update_time is None:
                print(f"{file_path} 未找到提交记录，跳过处理")
                continue
            with open(file_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    result = re.search(modification_date_pattern, line)
                    if result:
                        current_date = result.groups(1)[0]
                        if current_date == update_time:
                            print(f"{file_path} 日期已为最新。")
                            break
                        else:
                            lines[i] = f':material-clock-edit-outline:{{ title="修改日期" }} {update_time}\n'
                            f.seek(0)
                            f.writelines(lines)
                            print(f"{file_path} 日期已更新为：{update_time}")
                            break
                else:
                    lines.append(f'\n\n---\n\n:material-clock-edit-outline:{{ title="修改日期" }} {update_time}\n:material-clock-plus-outline:{{ title="创建日期" }} {create_time}\n')
                    f.seek(0)
                    f.writelines(lines)
                    print(f"{file_path} 未找到日期信息，已添加")
            print("-----------------------------------------------------------")


if __name__ == "__main__":
    docs_dir = os.path.join(os.getcwd(), "docs")

    # 排除不需要更新的目录或文件
    exclude_paths = [
        os.path.join(docs_dir, "example_file.md"),
        os.path.join(docs_dir, "example_directory"),
    ]
    repo_owner = "repo_owner" # 修改为代码库所有者
    repo_name = "repo_name" # 修改为代码库名称

    github_token = os.environ.get("GITHUB_TOKEN")

    update_markdown_files(docs_dir, exclude_paths, repo_owner, repo_name, github_token)
