import requests


def get_all_issues(base_url, headers):
    all_issues = []  # 用于存储所有issues
    page = 1  # 初始页码
    while True:  # 循环直到没有更多页
        params = {
            'page': page,
            'participant_category': 'all',
            'category': 'all',
            'limit': 15  # 每页显示的issues数量
        }
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # 添加当前页的issues到列表
            all_issues.extend(data.get('issues', []))
            # 检查是否还有更多页
            if page * params['limit'] >= data['total_count']:
                break  # 如果没有更多页，则退出循环
            page += 1  # 准备获取下一页
        else:
            print('请求失败，状态码:', response.status_code)
            break
    return all_issues


# 设置请求的URL（API端点）
url = 'https://gitlink.org.cn/api/v1/xuos/xiuos/issues'

# 设置请求头部，以避免使用缓存的内容
headers = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

# 获取所有issues
issues = get_all_issues(url, headers)

# 打印所有issues的详细信息
for issue in issues:
    title = issue.get('subject', 'No title provided')
    number = issue.get('project_issues_index', 'No number provided')
    state = issue.get('status_name', 'No state provided')
    created_at = issue.get('created_at', 'No creation date provided')

    print(f"Issue #{number}: {title}")
    print(f"State: {state}")
    print(f"Created at: {created_at}")
    print('-' * 60)
