import math
#import pandas as pd

file = open("AviationData.txt","r")

# Reading and storing the file into a list of strings (separated by "\n" by default).
aviation_data = file.readlines()

# Reading and storing the file into a list of list of words (separated by " | "
aviation_list = []
for line in aviation_data:
    aviation_list.append(line.split(" | "))

lax_code = []

for row in aviation_list:
    if 'LAX94LA336' in row:
        lax_code.append(row)

# This kind of search has a time complexity of o(amount_rows*amount_columns) bilinear (since loops through eah row first and then loops through each item in the row. 


# Linear time algorithm to serch the lax-code
# using the aviation_data string directly
cont = 0
number_line = []
for line in aviation_data: 
    if 'LAX94LA336' in line:
        number_line.append(cont)    
    cont +=1
print(number_line)
print("SEPARACIÓN")


#log(n) time algorithm that searches lax-code
# Binary search:
# Ordering each line temporarily:
temporary_list = []
for each in aviation_list:
    sorted_words = sorted(each)
    temporary_list.append(sorted_words)

def search_string(lista,string): 
    length = len(lista)    
    upper_bound = length - 1
    lower_bound = 0
    
    index = math.floor((upper_bound+lower_bound)/2)
    guess = lista[index]
    
    while string != guess and lower_bound <= upper_bound:
       
        if string < guess: 
            upper_bound = index - 1
            lower_bound = lower_bound
            index = math.floor((upper_bound+lower_bound)/2)
            guess = lista[index]
        elif string > guess: 
            upper_bound = upper_bound
            lower_bound = index + 1
            index = math.floor((upper_bound+lower_bound)/2)
            guess = lista[index]
    
    if string == guess: 
        return lista
    else: 
        return -1

lax_list = []
for lista in temporary_list:
    to_append = search_string(lista,"LAX94LA336")
    if to_append == -1:
        continue
    lax_list.append(to_append)    

aviation_dict_list = [] 

columns_names = aviation_data[0].split(" | ")

for each in aviation_data: 
    row = each.split(" | ")
    dictionary = {}
    for i,value in enumerate(row):   
        dictionary[columns_names[i]]=value
    
    aviation_dict_list.append(dictionary)            

lax_dict = []
for dictionary in aviation_dict_list:
    if "LAX94LA336" in dictionary.values():
        lax_dict.append(dictionary)
        
# Searching and counting accidents by state:
# We are going to use the dictionary representation
state_accidents = {}
for each in aviation_dict_list:
    state = (each["Location"].split(","))[0]
    if state in state_accidents:
        state_accidents[state] +=1
    else: state_accidents[state] = 1
        
maximo = 0
state_most_accidents = ""
for k,v in state_accidents.items():
    if v>maximo:
        maximo = v
        state_most_accidents = k
    else: continue 
print(state_most_accidents,"is the top state-airplane accidents with: ", maximo, "accidents.")

for each in aviation_dict_list:
    if each["Total Fatal Injuries"]=="": 
        each["Total Fatal Injuries"]="0"
    if each["Total Serious Injuries"]=="":
        each["Total Serious Injuries"]="0"
# Exploring the fatal injuries and serious injuris by month in the US.
# The Event Day column has the format month/day/year, for instance 09/05/2015. 

monthly_injuries = {}

for each in aviation_dict_list[1:]: # skip top line with column names
    date = each["Event Date"][:2]+"/"+each["Event Date"][-4:]
    """
    #If the int application doesn't work for some value 
    try: 
        int(each["Total Fatal Injuries"])
    except ValueError:
        print(each["Total Fatal Injuries"])
        break
    """
    if date in monthly_injuries:
        monthly_injuries[date] += (int(each["Total Fatal Injuries"]) + int(each["Total Serious Injuries"]))
    else: 
        monthly_injuries[date] = int(each["Total Fatal Injuries"]) + int(each["Total Serious Injuries"])
        
dates = monthly_injuries.keys()

# We are going to store all the years in a list
years = []
for date in dates: 
    if date[-4:] == "1981": 
        print(date)
    year = date.split("/")[1]
    
    years.append(year)
    
years = sorted(years)
print(len(years))

# results first isolated dates/years are: '10/1948', '07/1962', '08/1974', '06/1977', '08/1979', '08/1981'.
# The years with full month coverage goes from 1982 to 2015 
complete_ordered_dates = ["",'10/1948', '07/1962', '08/1974', '06/1977', '08/1979', '08/1981']

cont = 1
for year in years:
    
    if cont>12:
        cont=1
        
    if year>"1981":
        if cont<=9:
            m_y = "0{0}".format(cont) + "/" + year
            
            complete_ordered_dates += [m_y]
            
            cont += 1
        elif 9<cont and cont<=12: 
            m_y = "{0}".format(i) + "/" + year
            complete_ordered_dates += [m_y]   
            cont += 1
print(len(complete_ordered_dates))            

# CONTINUE IN NOTEBOOK, NEXT STEPS            
# Mapping out accidents using the basemap library for matplotlib.
# Counting the number of accidents by air carrier.
# Counting the number of accidents by airplane make and model.