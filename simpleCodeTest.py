# # Lets try to figure this out later


# def tri_recursion(k):
#   if(k > 0):
#     result = k + tri_recursion(k - 1)
#     print(result)
#   else:
#     result = 0
#   return result

# print("\n\nRecursion Example Results")
# tri_recursion(6)


# class Employee: 

#     def __init__(self, first, last, pay) -> None: 
#         self.first = first 
#         self.last = last 
#         self.email = first + '.' + last + '@email.com' 
#         self.pay = pay 

#     def fullname(self): 
#         return '{} {}'.format(self.first, self.last) 
    
#     def apply_raise(self):
#         self.pay = int(self.pay * 1.04)
 

# emp_1 = Employee('Corey', 'Schafer', 50000) 
# emp_2 = Employee('Bob', 'Builder', 55000) 

# print (emp_1.pay)
# emp_1.apply_raise()
# print(emp_1.pay)




# class Person:
#     def __init__(self, name, age, country):
#         self.name = name
#         self.age = age
#         self.country = country


# p1 = Person('John', 31, 'Norway')
# print(p1)

# x = vars(Person)
# print(x)
# print(p1.__dict__)



# import requests

# def GHTokenAuth():
#     username = 'rknupfer'
#     token = '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'
#     login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(username,token))

# GHTokenAuth()


import httpx
import csv
import json 

def gh_token_auth():
    username = 'rknupfer'
    token = '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'
    headers = {'authorization': f'Bearer {token}'}
    login = httpx.request(method='GET', url='https://api.github.com/orgs/optilogic/code-scanning/alerts', params={'per_page': 100, 'tool': 'CodeQL', 'state': 'open'}, headers=headers)
    try:
        json:list|None = login.json() # '|' is python 3.10 union operator
    
    # 'login' is an object of 'Response'. 
    # 'header' is property (attribute) of type 'Headers'
    # 'get' is a method of 'headers'
        link:str|None = login.headers.get('link')
        # for r in json:
        #     ["rule"]["security_severity_level"]
        # how to pull from json object: dictionary within a list
        with open('/home/r/gh_repos/output/codeqloutput.csv', 'w') as file:
            # Create a CSV dictionary writer and add the student header as field names
            writer = csv.DictWriter(file)
            # Use writerows() not writerow()
            # writer.writeheader()
            writer.writerows(json)
    except:
        json = None
        link = None
    return json, link
   
    # print(type(r))
    # pass
gh_token_auth()





