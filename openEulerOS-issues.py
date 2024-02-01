import requests
import pandas as pd
from bs4 import BeautifulSoup

# 设置 Gitee API 访问令牌
gitee_token = '1c6d9d944ddbf30dcb1af72a0cd5e351'
headers = {'Authorization': f'token {gitee_token}'}

# Gitee 仓库地址
repo_owner = 'openEuler'
repo_name = 'kernel'

# https://gitee.com/OpenCloudOS/OpenCloudOS-Kernel/issues
# Gitee API URL for issues
api_url = f'https://gitee.com/api/v5/repos/{repo_owner}/{repo_name}/issues'

# 存储所有问题记录的列表
all_issues = []

# 设置初始页码
current_page = 1

while True:
    # 发送 API 请求
    params = {'page': current_page, 'per_page': 100, 'state': 'open'}
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        issues_data = response.json()

        # 将当前页面的问题记录添加到列表
        all_issues.extend(issues_data)

        # 检查是否有下一页
        if len(issues_data) == 100:
            current_page += 1
        else:
            break  # 没有下一页，结束循环

    else:
        print(f"Failed to fetch issues. Status code: {response.status_code}")
        break  # 失败时结束循环

# 创建 DataFrame
df = pd.DataFrame(columns=['Issue Number', 'Author', 'Created At', 'Title'])

# 遍历所有问题记录数据
for issue in all_issues:
    issue_number = issue['number']
    issue_title = issue['title']
    issue_author = issue['user']['login']
    issue_created_at = issue['created_at']

    # 将数据添加到 DataFrame 中
    df = pd.concat([df, pd.DataFrame({'Issue Number': issue_number, 'Author': issue_author,
                                      'Created At': issue_created_at, 'Title': issue_title}, index=[0])], ignore_index=True)

# 将 DataFrame 写入 Excel 文件
excel_file_path = 'openEulerOS_issues.xlsx'
df.to_excel(excel_file_path, index=False)

print(f"Issues data has been written to {excel_file_path}")

