import requests
import json


def create_webhook(repo_name, webhook_url, access_token):
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "name": "web",
        "active": True,
        "events": ["*"],
        "config": {"url": webhook_url, "content_type": "json"},
    }
    response = requests.post(
        f"https://api.github.com/repos/{repo_name}/hooks",
        headers=headers,
        data=json.dumps(data),
    )
    if response.status_code == 201:
        print(f"成功为 {repo_name} 创建 Webhook")
    else:
        print(f"无法为 {repo_name} 创建 Webhook。状态码: {response.status_code}")
        print(response.text)


def main():

    access_token = "你的access_token"  # 你的access_token

    webhook_url = "你的Webhook地址"  # 你的Webhook地址

    # 初始化分页参数
    page = 1
    per_page = 30  # 每页多少个仓库，根据实际情况调整

    while True:
        # 获取当前页的仓库信息
        response = requests.get(
            "https://api.github.com/user/repos",
            headers={"Authorization": f"token {access_token}"},
            params={"per_page": per_page, "page": page},
        )
        if response.status_code == 200:
            repos = response.json()
            if not repos:  # 如果当前页没有仓库信息，说明已经获取完所有仓库
                break
            for repo in repos:
                repo_name = repo["full_name"]
                create_webhook(repo_name, webhook_url, access_token)
            page += 1
        else:
            print(f"无法获取仓库列表。状态码: {response.status_code}")
            print(response.text)
            break


if __name__ == "__main__":
    main()
