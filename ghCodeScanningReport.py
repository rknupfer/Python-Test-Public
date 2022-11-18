# Accessing the GitHub REST Api requires installation of PyGithub
import requests
import base64
import httpx
import csv
import time
import json
from github import Github 
from pprint import pprint

def get_auth_and_scan_codes():
    # username = 'rknupfer'
    token = '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'
    headers = {'authorization': f'Bearer {token}'}
    login = httpx.request(method='GET', url='https://api.github.com/orgs/optilogic/code-scanning/alerts', params={'per_page': 100, 'tool': 'CodeQL', 'state': 'open'}, headers=headers)
    
    # List variable scanCodes_json (with nested dictionaries):
    scanCodes_json = login.json()
    return scanCodes_json
    
    
def get_codescan_alert_counts():
    results:dict
    subsetDict:dict
    
    scanCodes_json = get_auth_and_scan_codes()
    
    for dictionary in scanCodes_json:
        try:
            seclevel = dictionary['state':]
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1 
            
            seclevel = dictionary['created_at':]
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1            
            
            seclevel = dictionary['updated_at':]
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1             

            seclevel = dictionary['fixed_at':]
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1 
            
            seclevel = dictionary['dismissed_by':]
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1 
            
            # Nested one deep            
            seclevel = dictionary['tool']['name']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1
            
            # Nested one deep
            # Some alerts don't have a security severity level
            seclevel = dictionary['rule']['security_severity_level']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1

            # Nested one deep
            seclevel = dictionary['repository']['name']
            #seclevel = f'repo:{seclevel}'
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1
            
        except KeyError:
            pass            
        
    for dictionary1 in scanCodes_json:
        try:
            for subsetDict in dictionary1.items():            
                if not subsetDict in dictionary1['state']:
                    subsetDict = dictionary1['state':[0]]
                
                if not subsetDict in dictionary1['created_at']:
                    subsetDict = dictionary1['created_at':[0]]           
                
                if not subsetDict in dictionary1['updated_at']:
                    subsetDict = dictionary1['updated_at':[0]]
                    
                if not subsetDict in dictionary1['fixed_at']:
                    subsetDict = dictionary1['fixed_at':[0]]              
                    
                if not subsetDict in dictionary1['dismissed_by']:
                    subsetDict = dictionary1['dismissed_by':[0]]               

                # Nested one deep                      
                if not subsetDict in dictionary1['tool']:
                    subsetDict = dictionary1['tool'['name':[0]]]
                    subsetDict = dictionary1['tool'['guid':[0]]]
                    subsetDict = dictionary1['tool'['version':[0]]]               

                # Nested one deep
                # Some alerts don't have a security severity level                
                if not subsetDict in dictionary1['rule':]:
                    subsetDict = dictionary1['rule'['id':[0]]]
                    subsetDict = dictionary1['rule'['severity':[0]]]
                    subsetDict = dictionary1['rule'['description':[0]]]
                    subsetDict = dictionary1['rule'['name':[0]]]
                    subsetDict = dictionary1['rule'['tags':[0]]]
                    subsetDict = dictionary1['rule'['security_severity_level':[0]]]                  

                # Nested one deep                      
                if not subsetDict in dictionary1['repository']:
                    subsetDict = dictionary1['repository'['id':[0]]]
                    subsetDict = dictionary1['repository'['node':[0]]]    
                    subsetDict = dictionary1['repository'['name':[0]]]    
                    subsetDict = dictionary1['repository'['full_name':[0]]]    
                    subsetDict = dictionary1['repository'['private':[0]]]                       
        
        except KeyError:
            pass            
        
    return results, subsetDict

def print_codescan_alert_counts():
    get_codescan_alert_counts()


def main():
    print_codescan_alert_counts()
    
if __name__ == '__main__':
    main()
    
    