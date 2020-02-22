import datetime
import sys

cli_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-cli+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22+-label:%22Feature%20Request%22"
extension_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-cli-extensions+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22+-label:%22Feature%20Request%22"
powershell_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-powershell+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22+-label:%22Feature%20Request%22"
spec_api_base_url = "https://api.github.com/search/issues?q=repo:Azure/azure-rest-api-specs+is:issue+state:open+created:%3E{}+sort:created-asc+-label:%22Service%20Attention%22+-label:%22Feature%20Request%22"


cli_base_url= "https://github.com/Azure/azure-cli/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+-created%3A%3C{}+sort%3Acreated-asc+assignee%3A%40me"
extension_base_url = "https://github.com/Azure/azure-cli-extensions/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+-created%3A%3C{}+sort%3Acreated-asc+assignee%3A%40me"


days_before = 90
datetime_fromat = '%Y-%m-%dT%H:%M:%SZ'
date_format = '%Y-%m-%d'

def generate_issue_report():
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=days_before)
    start_date_str = start_date.strftime(date_format)
    issues = []
    issues.extend(get_issues(cli_api_base_url, start_date_str))
    issues.extend(get_issues(extension_api_base_url, start_date_str))
    issues.extend(get_issues(powershell_api_base_url, start_date_str))
    issues.extend(get_issues(spec_api_base_url, start_date_str))

    issues.sort(key=lambda issue: issue['created_at'])

    file_name = "OKR_3.2_issues.csv"
    with open(file_name, "w", encoding='utf-8') as f:
        f.write('title,assignees,target_date,created_date,url,repo\n')
        for issue in issues:
            html_url = issue['html_url']
            title = issue['title']
            title = title.replace('"', '""').replace("--", "'--")  # fix excel formula
            assignees = ','.join(assignee['login'] for assignee in issue['assignees'])
            created_at = issue['created_at']
            created_date = datetime.datetime.strptime(created_at, datetime_fromat)
            target_date = created_date + datetime.timedelta(days=days_before)
            repo = '/'.join(issue['repository_url'].split('/')[-2:])
            f.write(f'"{title}","{assignees}","{target_date.strftime(date_format)}","{created_date.strftime(date_format)}",=HYPERLINK("{html_url}"),"{repo}"\n')
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

def get_issues(api_base_url, start_date_str):
    import requests
    import json
    page = 1
    issues = []
    while True:
        issues_url = api_base_url.format(start_date_str)+ "&page={}".format(page)
        print(f"Request url: {issues_url}")
        response = requests.get(issues_url)
        if response.status_code != 200:
            raise Exception("Request to {} failed with {}".format(issues_url, response.status_code))
        items = json.loads(response.content.decode('utf-8'))['items']
        if len(items) == 0:
            break
        issues.extend(items)
        page += 1
    return issues


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python list_okr_3_2_issues.py report | python list_okr_3_2_issues.py web")
        sys.exit(1)
    _type = sys.argv[1]
    if _type == "report":
        generate_issue_report()
    elif _type == "web":
        open_github_my_issues()
    else:
        print("Usage: python list_okr_3_2_issues.py report | python list_okr_3_2_issues.py web")
