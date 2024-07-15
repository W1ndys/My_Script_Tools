import requests
import json
import time  # 导入时间模块


def delete_webhook(repo_name, webhook_url, access_token):
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    # 获取指定仓库的 Webhooks
    response = requests.get(
        f"https://api.github.com/repos/{repo_name}/hooks",
        headers=headers,
    )
    if response.status_code == 200:
        webhooks = response.json()
        for webhook in webhooks:
            if webhook["config"]["url"] == webhook_url:
                # 删除指定 Webhook
                response_delete = requests.delete(
                    f"https://api.github.com/repos/{repo_name}/hooks/{webhook['id']}",
                    headers=headers,
                )
                if response_delete.status_code == 204:
                    print(f"成功删除 {repo_name} 的指定 Webhook")
                else:
                    print(
                        f"无法删除 {repo_name} 的指定 Webhook。状态码: {response_delete.status_code}"
                    )
                    print(response_delete.text)
                break
        else:
            print(f"{repo_name} 中未找到指定的 Webhook")
    else:
        print(f"无法获取 {repo_name} 的 Webhooks。状态码: {response.status_code}")
        print(response.text)

    # 添加延迟，以减慢请求频率
    time.sleep(2)  # 等待2秒钟，防止请求过于频繁


def delete_all_webhooks(webhook_url, access_token):
    page = 1
    per_page = 30  # 根据实际情况调整每页的数量

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
                delete_webhook(repo_name, webhook_url, access_token)
            page += 1
        else:
            print(f"无法获取仓库列表。状态码: {response.status_code}")
            print(response.text)
            break


if __name__ == "__main__":

    access_token = "你的access_token"  # 你的access_token

    webhook_url = "你的Webhook地址"  # 你的Webhook地址

    delete_all_webhooks(webhook_url, access_token)
