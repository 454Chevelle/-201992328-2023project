import requests
import time

# 设置请求的URL（API端点）
url = 'https://gitlink.org.cn/api/v1/xuos/xiuos/commits'

# 设置查询参数
params = {
    'sha': '2023_open_source_contest',  # 分支名
    'page': 1,  # 页码
    'limit': 10  # 每页数量
}

# 发送GET请求获取提交记录
response = requests.get(url, params=params)

# 检查状态码
if response.status_code == 200:
    # 解析返回的数据
    commits_data = response.json()
    commits = commits_data['commits']

    # 遍历commits列表，打印每个commit的详细信息
    for commit in commits:
        # 提取commit信息
        message = commit['commit_message']
        sha = commit['sha']
        author = commit['author']['name']
        commit_time = commit['commit_time']
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(commit_time))

        # 打印详细信息
        print(f"Commit {sha}: {message.strip()}")
        print(f"Author: {author}")
        print(f"Date: {date}")
        print('-' * 60)
else:
    print('请求失败，状态码:', response.status_code)
