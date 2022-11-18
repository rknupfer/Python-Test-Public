#Done while watching Corey Shafer: Python OOP Tutorial 1: Classes and Instances on YouTube
#https://www.youtube.com/watch?v=ZDa-Z5JzLYM&list=PL-osiE80TeTsqhIuOqKhwlXsIBIdSeYtc

# Python Definitions

# Object :
# object is one of instances of the class. which can perform the functionalities which are defined in the class.

#Difference between method and function
# 1. Simply, function and method both look similar as they perform in almost similar 
# way, but the key difference is the concept of ‘Class and its Object‘.
# 2.  A Function can be called only by its name, as it is defined independently. But 
# a method can’t be called by its name only, we need to invoke the class by a 
# reference of that class in which it is defined, i.e. method is defined within a 
# class and hence they are dependent on that class.


# Python Method

# Method is called by its name, but it is associated to an object (dependent).
# A method definition always includes ‘self’ as its first parameter.
# A method is implicitly passed the object on which it is invoked.
# It may or may not return any data.
# A method can operate on the data (instance variables) that is contained by the corresponding class


# Basic Python method 
class class_name
    def method_name () :
        ......
        # method body
        ......  
        

# Python 3  User-Defined  Method
class ABC :
    def method_abc (self):
        print("I am in method_abc of ABC class. ")
  
class_ref = ABC() # object of ABC class
class_ref.method_abc()
      

# Python 3 Inbuilt method : 

import math
  
ceil_val = math.ceil(15.25)
print( "Ceiling value of 15.25 is : ", ceil_val) 












#Class declaration with class variables

# The __init__() function is called automatically every time the class is being used to create a new object.
# Class initializer or constructor
# A Class is like an object constructor, or a "blueprint" for creating objects.
# A template or cookie cutter
        
# self :
# self represents the instance of the class. By using the "self" keyword we can access the attributes and methods of the class in python.

# __init__ :
# "__init__" is a reseved method in python classes. It is known as a constructor in object oriented concepts. This method called when an object is created from the class and it allow the class to initialize the attributes of a class.


# Example 1:
class MyClass:
    x = 5

print(MyClass.x)


# Example 2:
class Employee:
    def __init__(self) -> None: 
        pass #skip for now, good for placeholder for an empty class

#Class instances with instance variables
emp_1 = Employee()
emp_2 = Employee()

emp_1.first = 'Corey'
emp_1.last = 'Shafer'
emp_1.email = 'Corey.Shafer@company.com'
emp_1.pay = 50000

emp_1.first = 'Tim'
emp_1.last = 'Hawkins'
emp_1.email = 'Shelly.Hawkins@company.com'
emp_1.pay = 51000


print(emp_1.email)
print(emp_2.email)
print('{} {}'.format(emp_1, 'Schafer'))

# #Example 3
# class Employee:
#     def __init__(self, first, last, pay) -> None:
#        self.first = first
#        self.last = last
#        self.email = first + '.' + last + '@email.com'
#        self.pay = pay
       
#     def fullname (self):
#         return '{} {}'.format(self.first, self.last)
    
# emp_1 = Employee('Corey', 'Schafer', 50000)
# emp_2 = Employee('Bob', 'Builder', 55000)

# print(emp_1.email)
# print(emp_2.email)
# print(emp_1.fullname)



