# Accessing the GitHub REST Api requires installation of PyGithub
import httpx
import github
import pprint
import json
from pydantic import BaseModel, Field
import pandas as pd
import numpy as np
import time


class Tool(BaseModel):
    """The tool that found the alert"""

    


def get_auth_and_scan_codes():
    # file deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
    token = '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'
    headers = {'authorization': f'Bearer {token}'}
    login = httpx.request(method='GET', url='https://api.github.com/orgs/optilogic/code-scanning/alerts', params={'per_page': 100, 'tool': 'CodeQL', 'state': 'open'}, headers=headers)
    
    # List variable scanCodes_json (with nested dictionaries):
    scanCodes_json = login.json()
    return scanCodes_json
    
    
def get_codescan_alert_counts():
    results:dict = {}
    results01:dict = {}
    seclevel:str = ''
   
    scanCodes_json = get_auth_and_scan_codes()
        
    for dictionary in scanCodes_json:
        try:
            seclevel = dictionary['state']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1
            
            seclevel = dictionary['created_at']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1            
            
            seclevel = dictionary['updated_at']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1             

            seclevel = dictionary['fixed_at']
            if not seclevel in results.keys():
                results[seclevel] = 1
            results[seclevel] = results[seclevel] + 1 
            
            seclevel = dictionary['dismissed_by']
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
            seclevel = dictionary1['state']
            if not seclevel in results01.keys():
                results01 = dict(state=seclevel)
                # results01['state'] = seclevel
                #ids_to_return_dict = {'children':[{'id':value}]}
                
        
                                                
        except KeyError:
            pass            
        
    return results, results01


def print_codescan_alert_counts():
    results, results01 = get_codescan_alert_counts()
    
    test:str
    repo:str
    count:str
    try:
        print(f'Number of Grype alerts: {results["Grype"]}')
        print(f'Number of Severity alerts: {results["security_severity_level"]}')
        
        print(f'Security severity level count - low: {results["low"]}') 
        print(f'Security severity level count - medium: {results["medium"]}') 
        print(f'Security severity level count - high: {results["high"]}') 
        print(f'Security severity level count - critical: {results["critical"]}') 

        print(f'Number of alerts open: {results["open"]}')
        print(f'Number of alerts closed: {results["closed"]}')
        print(f'Number of dismissed alerts: {results["dismissed_by"]}')
        print(f'Number of alerts fixed: {results["fixed"]}') 
            
    except KeyError:
        pass     
        
    for x in results.items():
        try:
            print(f'Number of alerts fixed: {results["repository"]["name"]}') 
            
        except KeyError:
            pass     

    for x in results01.items():   
        try:
            repo = results01["repository"]["name"]
            count = results["repository"][repo]
            print (f'{repo}:{count}')            
            
        except KeyError:
            pass    


def main():
    print_codescan_alert_counts()

    
if __name__ == '__main__':
    main()