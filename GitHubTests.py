
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
    
    scanCodes_json:list = []
    results:dict = {}
    repoDict:dict = {}
       
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
            seclevel = dictionary['tool']   #['name']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1
            
            # Nested one deep
            # Some alerts don't have a security severity level
            seclevel = dictionary['rule']   #['security_severity_level']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1

            # Nested one deep
            seclevel = dictionary['repository']   #['name']
            #seclevel = f'repo:{seclevel}'
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1
            
        except KeyError:
            pass            

    


    # Pull repo and no. of alerts and create dictionary repoDict
    # for key, value in results.items(): # and key is not None and key is None and value is None:
    #     if key is not None:
    #         stKey:str = key
    #         stValue:str = value
    #         try:
    #             if stKey.find('repo:') != -1: 
    #                 stKey = stKey.replace('repo:', '')
                    
    #                 # Either add (repoDict.update) or update the repotDict dictionary key:value pair
    #                 if stKey in repoDict:
    #                     repoDict = {stKey:stValue}
    #                 else:
    #                     repoDict.update({stKey:stValue})
    #             else:
    #                 pass
    #         except KeyError:
                
    #             pass
    #     else:
    #         pass
        
    return results


def print_codescan_alert_counts():
    
    results = get_codescan_alert_counts()
    
    stSeverity:str = "Security severity level count - "
    stScannerAlerts:str = "Number of alerts per scanner - "
    stRepoAlerts:str

    for dictionary in results:
        try:
            # stKey:str = key
            # stValue:str = value   
    
            if key = stSeverity:
                stSeverity += f' {key}:{value} '
            elif key = stScannerAlerts:
                stScannerAlerts += f' {key}:{value} '
            elif stKey.find('repo:') != -1: 
                stKey = stKey.replace('repo:', '')
 
                
                
                
                
            print(stSeverity)
            # print(f'Security severity level count - low: {results["low"]}, medium: {results["medium"]}, high: {results["high"]}, critcal: {results["critical"]}') 
            print(f'Number of Grype alerts: {results["Grype"]}')
    except KeyError:
        pass    
        
    try:
        print(f'Alerts per repository - {repoDict}')
    except KeyError:
        pass    
    
    
def main():
    print_codescan_alert_counts()
    
if __name__ == '__main__':
    main()

