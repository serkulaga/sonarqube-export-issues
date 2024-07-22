import pandas as pd
import requests
import base64
from datetime import datetime, timedelta
import argparse
import os
import fnmatch

def export(sonarqube_url, auth_token, project_pattern):

    current_date = datetime.now()

    auth = base64.b64encode(f'{auth_token}:'.encode()).decode()
    headers = {'Authorization': f'Basic {auth}'}

    response = requests.get(sonarqube_url + '/api/projects/search', headers=headers)

    print('Fetching projects...')
    projects = []
    if response.status_code == 200:
        try:
            data = response.json()
            projects = data.get('components', [])
        except requests.exceptions.JSONDecodeError as e:
            print(f'Failed to parse JSON response: {e}, Response content {response.text}')
    else:
        print(f'Failed to retrieve projects: {response.status_code}, content: {response.text}')

    print(f'Projects count: {len(projects)}')
    
    for project in projects:
        project_key = project['key'] 
        if project_pattern and not fnmatch.fnmatch(project_key, project_pattern):
            print(f'Skip project by pattern: {project_key}')
            continue;

        print(f'Fetching issues for project: {project_key}')
        issues = get_all_issues_by_project(project_key, sonarqube_url, headers)
        print(f'Issues count: {len(issues)}')
        if issues:
            df = pd.DataFrame(issues)
            excel_file_name = f'sonarqube_issues_{project_key}_{current_date.strftime('%Y%m%d')}.xlsx'
            df.to_excel(excel_file_name, index=False)
            print(f'Saved to excel file: {excel_file_name}')

def get_all_issues_by_project(project_key, sonarqube_url, headers):
    page = 1
    page_size = 500  # Maximum allowed by SonarQube is usually 500

    issues = []
    page = 1
    while True:
        params = {
            'componentKeys': project_key,
            'ps': page_size,
            'p': page
        }

        response = requests.get(sonarqube_url + '/api/issues/search', params=params, headers=headers)
        if response.status_code == 200:
            
            try:
                data = response.json()
                issues.extend(data.get('issues', []))
            except requests.exceptions.JSONDecodeError as e:
                print(f'Failed to parse JSON response: {e}, Response content {response.text}')
        else:
            print(f'Failed to retrieve issues: {response.status_code}, content: {response.text}')

        # Check if there are more pages
        if page * page_size >= data['paging']['total']:
            break 

        page += 1

    return issues


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--sonarqube_export_url", type=str, default=os.environ.get('SONARQUBE_EXPORT_URL', 'http://localhost:9000'))
    parser.add_argument("--sonarqube_export_auth_token", type=str, default=os.environ.get('SONARQUBE_EXPORT_AUTH_TOKEN'))
    parser.add_argument("--project_pattern", type=str, default="*", help="wildcard pattern, default all")

    args = parser.parse_args()

    export(args.sonarqube_export_url, args.sonarqube_export_auth_token, args.project_pattern)


if __name__ == "__main__":
    main()
