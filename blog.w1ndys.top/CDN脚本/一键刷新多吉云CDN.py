import os
import json
from datetime import datetime

from hashlib import sha1
import hmac
import requests
import urllib


def load_daily_counts():
    """
    加载每日计数数据，如果文件不存在则返回一个空的计数字典

    :return dict: 包含每日计数的字典
    """
    counts_file = "daily_counts.json"
    if os.path.exists(counts_file):
        with open(counts_file, "r") as f:
            return json.load(f)
    else:
        return {"date": "", "counts": {"url": 0, "path": 0, "prefetch": 0}}


def save_daily_counts(counts):
    """
    保存每日计数数据到本地文件

    :param dict counts: 包含每日计数的字典
    """
    counts_file = "daily_counts.json"
    with open(counts_file, "w") as f:
        json.dump(counts, f)


def increment_count(counts, operation):
    """
    增加指定操作类型的计数

    :param dict counts: 包含每日计数的字典
    :param str operation: 操作类型
    """
    counts["counts"][operation] += 1


def reset_counts(counts, current_date):
    """
    重置计数器

    :param dict counts: 包含每日计数的字典
    :param str current_date: 当前日期（格式为 YYYY-MM-DD）
    """
    counts["date"] = current_date
    counts["counts"] = {"url": 0, "path": 0, "prefetch": 0}


def dogecloud_api(api_path, data={}, json_mode=False):
    """
    调用多吉云API

    :param api_path:    调用的 API 接口地址，包含 URL 请求参数 QueryString，例如：/console/vfetch/add.json?url=xxx&a=1&b=2
    :param data:        POST 的数据，字典，例如 {'a': 1, 'b': 2}，传递此参数表示不是 GET 请求而是 POST 请求
    :param json_mode:   数据 data 是否以 JSON 格式请求，默认为 false 则使用表单形式（a=1&b=2）

    :type api_path: string
    :type data: dict
    :type json_mode bool

    :return dict: 返回的数据
    """

    # 这里替换为你的多吉云永久 AccessKey 和 SecretKey，可在用户中心 - 密钥管理中查看
    # 请勿在客户端暴露 AccessKey 和 SecretKey，否则恶意用户将获得账号完全控制权
    access_key = "xxxxx"
    secret_key = "xxxxxxxxxx"

    # 构造请求正文和 MIME 类型
    if json_mode:
        body = json.dumps(data)
        mime = "application/json"
    else:
        body = urllib.parse.urlencode(data)
        mime = "application/x-www-form-urlencoded"

    # 构造签名字符串并计算签名
    sign_str = api_path + "\n" + body
    signed_data = hmac.new(secret_key.encode("utf-8"), sign_str.encode("utf-8"), sha1)
    sign = signed_data.digest().hex()

    # 构造 Authorization 头部
    authorization = "TOKEN " + access_key + ":" + sign

    # 发起请求
    response = requests.post(
        "https://api.dogecloud.com" + api_path,
        data=body,
        headers={"Authorization": authorization, "Content-Type": mime},
    )

    # 返回响应的 JSON 数据
    return response.json()


def select_operation():
    """
    用户选择操作类型

    :return string: 用户选择的操作类型
    """
    print("请选择操作类型：")
    print("1. 刷新 URL 操作")
    print("2. 刷新目录操作")
    print("3. 预热 URL 操作")
    choice = input("请输入选项（1/2/3）：")
    if choice in ["1", "2", "3"]:
        return choice
    else:
        print("无效的选择")
        return None


# 获取当前日期（格式为 YYYY-MM-DD）
current_date = datetime.now().strftime("%Y-%m-%d")

# 加载每日计数数据
counts = load_daily_counts()

# 检查是否需要重置计数器（如果当前日期与记录的日期不同）
if counts.get("date") != current_date:
    reset_counts(counts, current_date)

# 获取用户选择的操作类型
rtype_choice = select_operation()
if rtype_choice:
    # 根据操作类型构造数据
    if rtype_choice == "1":
        rtype = "url"
        urls_input = input("请输入需要刷新的 URL 列表，以逗号分隔：")
    elif rtype_choice == "2":
        rtype = "path"
        urls_input = input("请输入需要刷新的目录列表，以逗号分隔：")
    else:
        rtype = "prefetch"
        urls_input = input("请输入需要预热的 URL 列表，以逗号分隔：")

    url_list = urls_input.split(",")

    # 检查是否超过每日限额
    if counts["counts"][rtype] >= 1000 and rtype == "url":
        print("刷新 URL 操作次数已达每日上限（1000次）")
    elif counts["counts"][rtype] >= 20 and rtype == "path":
        print("刷新目录操作次数已达每日上限（20次）")
    elif counts["counts"][rtype] >= 1000 and rtype == "prefetch":
        print("预热 URL 操作次数已达每日上限（1000次）")
    else:
        # 调用多吉云API刷新 CDN 缓存
        api = dogecloud_api(
            "/cdn/refresh/add.json", {"rtype": rtype, "urls": json.dumps(url_list)}
        )

        # 处理响应结果
        if api["code"] == 200:
            print("任务 ID:", api["data"]["task_id"])
            # 更新计数
            increment_count(counts, rtype)
            save_daily_counts(counts)
            # 输出剩余次数
            remaining_counts = {
                "url": max(0, 1000 - counts["counts"]["url"]),
                "path": max(0, 20 - counts["counts"]["path"]),
                "prefetch": max(0, 1000 - counts["counts"]["prefetch"]),
            }
            print("剩余次数：", remaining_counts)
        else:
            print("API 失败：" + api["msg"])

# 按 Enter 键退出
input("按 Enter 键退出...")
