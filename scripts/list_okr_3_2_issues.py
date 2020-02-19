import datetime
import sys

cli_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-cli+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22"
extension_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-cli-extensions+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22"
cli_base_url= "https://github.com/Azure/azure-cli/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+-created%3A%3C{}+sort%3Acreated-asc+assignee%3A%40me"
extension_base_url = "https://github.com/Azure/azure-cli-extensions/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+-created%3A%3C{}+sort%3Acreated-asc+assignee%3A%40me"
    
days_before = 90
datetime_fromat = '%Y-%m-%dT%H:%M:%SZ'
date_format = '%Y-%m-%d'

def generate_issue_report():
    import requests
    import json
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_before)

    start_date_str = start_date.strftime(date_format)
    issues_url = cli_api_base_url.format(start_date_str)
    print(f"Request url: {issues_url}")
    response = requests.get(issues_url)
    if response.status_code != 200:
        raise Exception("Request to {} failed with {}".format(issues_url, response.status_code))
    issues = json.loads(response.content.decode('utf-8'))['items']

    issues_url = extension_api_base_url.format(start_date_str)
    print(f"Request url: {issues_url}")
    response = requests.get(issues_url)
    if response.status_code != 200:
        raise Exception("Request to {} failed with {}".format(issues_url, response.status_code))
    issues.extend(json.loads(response.content.decode('utf-8'))['items'])
    issues.sort(key=lambda issue: issue['created_at'])

    file_name = "OKR_3.2_issues.csv"
    with open(file_name, "w", encoding='utf-8') as f:
        f.write('title,assignees,target_date,created_date,url\n')
        for issue in issues:
            html_url = issue['html_url']
            title = issue['title']
            title = title.replace('"','""')
            assignees = ','.join(assignee['login'] for assignee in issue['assignees'])
            created_at = issue['created_at']
            created_date = datetime.datetime.strptime(created_at, datetime_fromat)
            target_date = created_date + datetime.timedelta(days=days_before)
            f.write(f'"{title}","{assignees}","{target_date.strftime(date_format)}","{created_date.strftime(date_format)}","{html_url}"\n')
    print(f"Report generated in {file_name}")

def open_github_my_issues():
    import webbrowser
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_before)
    start_date_str = start_date.strftime(date_format)
    url = extension_base_url.format(start_date_str)
    webbrowser.open_new_tab(url)
    url = cli_base_url.format(start_date_str)
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python list_okr_3_2_issues.py report | python list_okr_3_2_issues.py web")
        sys.exit(1)
    type = sys.argv[1]
    if type == "report":
        generate_issue_report()
    elif type == "web":
        open_github_my_issues()
    else:
        print("Usage: python list_okr_3_2_issues.py report | python list_okr_3_2_issues.py web")
