import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sendingEmails import sendEmail

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("Course Exchange-a3d41b4be1aa.json", scope)
client = gspread.authorize(creds)

sheet = client.open("COURSE EXCHANGE (Responses)").sheet1
record = sheet.get_all_records()

coursesDataframe = pd.DataFrame(record)
#coursesDataframe = coursesDataframe.drop_duplicates(subset=['Email Address', 'Supply','Demand'])
#Remove

def cleanUpDemandSupply(course):
    course = course.split(" ") #SPLITTING ON - HERE REMEMBER
    if len(course) == 3 and course[1].isnumeric() and course[0].isalpha() and course[2].isalpha():
        course  = " ".join(course)
        return course
    else:
        return ""

coursesDataframe["Demand"] = coursesDataframe["Demand"].apply(cleanUpDemandSupply)
coursesDataframe["Supply"] = coursesDataframe["Supply"].apply(cleanUpDemandSupply)

coursesDataframe.drop("Timestamp", inplace = True, axis = 1)
print(coursesDataframe)

from customerClass import Customer
from time import time
t1 = time()

array = np.array(coursesDataframe)

completePool = dict()
demand = set()
supply = set()
for entry in array:
    email = entry[0] #Email cant be in UPPER
    suppliedCourse = entry[1].upper()
    demandedCourse = entry[2].upper()

    customer = Customer("SAWAIZ", email, suppliedCourse, demandedCourse) #GET NAME TOO MAYBE?

    supply.add(suppliedCourse)

    demand.add(demandedCourse)

    if suppliedCourse not in completePool:
        completePool[suppliedCourse] = dict()
        completePool[suppliedCourse]["Demander"] = set()
        completePool[suppliedCourse]["Supplier"] = set()
        completePool[suppliedCourse]["Supplier"].add(customer)
    else:
        completePool[suppliedCourse]["Supplier"].add(customer)
        
    if demandedCourse not in completePool:
        completePool[demandedCourse] = dict()
        completePool[demandedCourse]["Demander"] = set()
        completePool[demandedCourse]["Supplier"] = set()
        completePool[demandedCourse]["Demander"].add(customer)
    else:
        completePool[demandedCourse]["Demander"].add(customer) 

def exchangePossible(supplier,demander):
    if supplier.getSupply() == demander.getDemand() and demander.getSupply() == supplier.getDemand():
        return True
    else:
        return False

demandSupplyIntersection = demand.intersection(supply)
for course in demandSupplyIntersection:
    demanderSet = completePool[course]["Demander"]
    supplierSet = completePool[course]["Supplier"]
    demandersToRemove = set() #Has to be a set because it will stop duplication
    suppliersToRemove = set()
    for demander in demanderSet:
        #ADD COURSE
        message = "For " + course + ", an exchange is possible with the following people. You can contact them if you want:\n"
        poss = False
        for supplier in supplierSet:
            if exchangePossible(supplier, demander):
                suppliersToRemove.add(supplier)
                poss = True
                message += supplier.email + "\n"
        if poss:
            message += "DISCLAIMER: THIS PLATFORM IS ONLY RESPONSIBLE FOR HELPING YOU CONTACT PEOPLE WHO MIGHT BE INTERESTED IN EXCHANGING COURSES WITH YOU. WE WILL NOT BE RESPONSIBLE FOR ANY INCONVINIENCES."
            sendEmail("POSSIBLE COURSE EXCHANGE FOR COURSE: " + course, message, [demander.email])
            demandersToRemove.add(demander)

    for demander in demandersToRemove:
        demanderSet.remove(demander)

    for supplier in suppliersToRemove:
        supplierSet.remove(supplier)

print(completePool)
t2= time()
print(t2-t1)


