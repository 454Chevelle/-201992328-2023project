import requests
import pandas as pd

# 设置 Gitee API 访问令牌
gitee_token = '1c6d9d944ddbf30dcb1af72a0cd5e351'
headers = {'Authorization': f'token {gitee_token}'}

# Gitee 仓库地址
repo_owner = 'OpenCloudOS'
repo_name = 'OpenCloudOS-Kernel'
branch_name = 'master'

# 初始化页码和 DataFrame
page = 1
df = pd.DataFrame(columns=["提交SHA", "作者", "日期", "消息"])

while True:
    # Gitee API URL
    api_url = f'https://gitee.com/api/v5/repos/{repo_owner}/{repo_name}/commits'
    params = {'ref_name': branch_name, 'page': page}

    # 发送 API 请求
    try:
        response = requests.get(api_url, headers=headers, params=params)
        response.raise_for_status()

        commits_data = response.json()

        if not commits_data:
            # No more data, break the loop
            break

        for commit in commits_data:
            commit_author = commit['commit']['author']['name']
            commit_date = commit['commit']['author']['date']
            commit_message = commit['commit']['message']
            commit_sha = commit['sha']

            # 使用 concat 函数将数据添加到 DataFrame
            df = pd.concat([df, pd.DataFrame({"提交SHA": [commit_sha], "作者": [commit_author], "日期": [commit_date], "消息": [commit_message]})])

        # 前进到下一页
        page += 1

    except requests.exceptions.RequestException as e:
        print(f"请求失败。错误: {e}")
        break

# 将 DataFrame 写入 Excel 文件
excel_file_path = 'opencloudOS_commits.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"提交数据已写入到 {excel_file_path}")
