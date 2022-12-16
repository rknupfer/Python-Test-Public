from dotenv import load_dotenv
import httpx
from pydantic import BaseModel, Field, validator
from os import getenv

load_dotenv()

PAT = getenv('PAT')

STATS: dict = {
    'total_alerts': 0,
    'severity_counts': {},
    'status_counts': {},
    'dismissed': 0,
    'tool_counts': {},
    'repository_counts': {},
    'average_alerts_per_repo': 0,
    }

class Repository(BaseModel):
    """Repository model"""
    name: str
    url: str

    class Config:
        frozen = True


class Rule(BaseModel):
    """Rule"""
    id: str = Field(..., alias='id')
    severity: str
    description: str
    security_severity_level: str

    class Config:
        frozen=True

    @validator('security_severity_level')
    def security_severity_level_validator(cls, v):
        if v in STATS['severity_counts'].keys():
            STATS['severity_counts'][v] += 1
        else:
            STATS['severity_counts'][v] = 1
        return v

class Tool(BaseModel):
    """The tool that found the alert"""
    name: str = Field(..., description="The name of the tool that found the alert")

    class Config:
        frozen=True

    @validator('name')
    def name_validator(cls, v):
        if v in STATS['tool_counts'].keys():
            STATS['tool_counts'][v] += 1
        else:
            STATS['tool_counts'][v] = 1

class CodeScanAlert(BaseModel):
    """Code scan alert"""
    id: int = Field(alias='number', description="Alert ID")
    state: str
    rule: Rule
    created_at: str
    dismissed_at: str | None
    html_url: str
    tool: Tool
    repository: Repository

    class Config:
        frozen=True

    @validator('state')
    def state_validator(cls, v):
        if v in STATS['status_counts'].keys():
            STATS['status_counts'][v] += 1
        else:
            STATS['status_counts'][v] = 1
        return v

    @validator('dismissed_at')
    def dismissed_at_validator(cls, v):
        if v is not None:
            STATS['status_counts']['dismissed'] += 1
        return v

    @validator('repository')
    def security_severity_level_validator(cls, v):
        if v.name in STATS['repository_counts'].keys():
            STATS['repository_counts'][v.name] += 1
        else:
            STATS['repository_counts'][v.name] = 1
        return v
    
    @validator('id')
    def id_validator(cls, v):
        STATS['total_alerts'] += 1
        return v

def calculate_aggregations():
    """Calculate aggregations"""
    repositories = get_repositories()
    STATS['average_alerts_per_repo'] = STATS["total_alerts"] / len(repositories)

def gh_api_call(url: str, method: str = 'GET', query_string: dict = None, data: dict = None):
    """Make a call to the GitHub API"""
    headers = {'authorization': f'Bearer {PAT}'}
    response = httpx.request(method, url, params=query_string, headers=headers, json=data)
    response.raise_for_status()
    try:
        json = response.json()
        link = response.headers.get('link')
    except:
        json = None
        link = None
    return json, link

def get_code_scan_alerts():
    """Get all code scan alerts"""
    all_alerts = []
    alerts = 1
    link = 'start'
    while alerts is not None and link is not None:
        alerts, link = get_code_scan_alert_page(link)
        if alerts is not None:
            all_alerts = list(set(alerts + all_alerts))
    return all_alerts

def get_code_scan_alert_page(link: str):
    """Get the code scan alert page"""
    alerts = []
    if link == 'start':
        page, link = gh_api_call('https://api.github.com/orgs/optilogic/code-scanning/alerts', method='GET', query_string={'per_page': 100, 'tool_name': 'CodeQL', 'state': 'open'})
    elif link is not None:
        links = {}
        parts = link.split(',')
        for p in parts:
            section = p.split(';')
            links[section[1].strip().replace('rel=', '').replace('"', '')] = section[0].strip()[1:-1]
        if 'next' in links.keys():
            page, link = gh_api_call(links['next'], method='GET', query_string={'per_page': 100, 'tool_name': 'CodeQL', 'state': 'open'})
        else:
            return None, None
    if len(page) == 0:
        return None, None
    for p in page:
        alerts.append(CodeScanAlert(**p))
    return alerts, link

def get_repositories():
    '''Get all repositories'''
    all_repositories = []
    repositories = 1
    link = 'start'
    while repositories is not None and link is not None:
        repositories, link = get_repositories_page(link)
        if repositories is not None:
            all_repositories = list(set(repositories + all_repositories))
    return all_repositories

def get_repositories_page(link: str):
    """Get the repository page"""
    repositories = []
    if link == 'start':
        page, link = gh_api_call('https://api.github.com/orgs/optilogic/repos', method='GET', query_string={'per_page': 100, 'type': 'all:'})
    elif link is not all:
        links = {}
        parts = link.split(',')
        for p in parts:
            section = p.split(';')
            links[section[1].strip().replace('rel=', '').replace('"', '')] = section[0].strip()[1:-1]
        if 'next' in links.keys():
            page, link = gh_api_call(links['next'], method='GET', query_string={'per_page': 100, 'type': 'all:'})
        else:
            return None, None
    if len(page) == 0:
        return None, None
    for p in page:
        if p['archived'] is False \
            and 'security_and_analysis' in p.keys() \
            and 'advanced_security' in p['security_and_analysis'].keys() \
            and p['security_and_analysis']['advanced_security']['status'] == 'enabled':
            repositories.append(Repository(**p))
    return repositories, link

def main():
    alerts = get_code_scan_alerts()
    # Simple Totals
    print(f'Number of alerts: {STATS["total_alerts"]}')
    print(f'Number of alerts by severity: {STATS["severity_counts"]}')
    print(f'Number of alerts by status: {STATS["status_counts"]}')
    print(f'Number of alerts dismissed: {STATS["dismissed"]}')
    print(f'Number of alerts by tool: {STATS["tool_counts"]}')
    print(f'Number of alerts by repository: {STATS["repository_counts"]}')

    # Aggregations
    calculate_aggregations()
    print(f'Average number of alerts per repository: {STATS["average_alerts_per_repo"]}')

if __name__ == '__main__':
    main()