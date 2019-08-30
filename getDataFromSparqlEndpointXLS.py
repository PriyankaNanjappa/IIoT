# !/usr/bin/env python2
# pip for python2(.7)
# pip install sparql-client

import sparql
# Writing to an excel  
# sheet using Python
import xlwt 
from xlwt import Workbook 
#from xlwt import Cell
# Combinations
from itertools import combinations

# Workbook is created 
wb = Workbook() 
  
# add_sheet is used to create sheets. 
Frameworks_Concerns = wb.add_sheet('Frameworks_Concerns',cell_overwrite_ok=True)
Classifications_Concerns = wb.add_sheet('Classifications_Concerns')
FW1_FW2 = wb.add_sheet('FW1_FW2',cell_overwrite_ok=True)

#SPARQL endpoint
s = sparql.Service('https://dydra.com/mtasnim/stoviz/sparql', "utf-8", "GET") ;


# Query all concerns
print("")
print("Query for Concerns:")
results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {?concern a sto_iot:Concern}") ;

concerns = []
i = 0;
for row in results :
    
    concerns.append(sparql.unpack_row(row)[0])
    concern_index = concerns.index(sparql.unpack_row(row)[0])
    Frameworks_Concerns.write(0,concern_index+1, sparql.unpack_row(row)[0])
    Classifications_Concerns.write(0,concern_index+1, sparql.unpack_row(row)[0])
    print(sparql.unpack_row(row)[0]);
    

# Query all frameworks 
print("")
print("Query for Frameworks:")
results = s.query("PREFIX sto: <https://w3id.org/i40/sto#> Select distinct ?framework where {?framework a sto:StandardizationFramework}") ;

frameworks = []
for row in results :
    frameworks.append(sparql.unpack_row(row)[0])
    print(sparql.unpack_row(row)[0]);


frameworksAndConcerns = [[ 0 for i in range(len(concerns))] for j in range(len(frameworks)) ]
for fw in frameworks :
    print("")
    print("Query Concerns for Framework " + fw)
    results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {<" + fw + "> sto_iot:frames ?concern}") ;  # sto:hasTargetConcern
    
    fw_index = frameworks.index(fw)
    # write framework URIs in column 0
    Frameworks_Concerns.write(fw_index+1,0, fw) 
    
           
    for row in results :
        try:
            concern_index = concerns.index(sparql.unpack_row(row)[0])
            frameworksAndConcerns[fw_index][concern_index] = 1
            Frameworks_Concerns.write(fw_index+1,concern_index+1, '1')
    
        except ValueError, error:
            print(error)
         

wb.save('xlwt example.xls')

print(frameworksAndConcerns)

   
# Blind spot: No frames link for a Concern 
Frameworks_Concerns.write(len(frameworks)+2,0, 'Blind Spot Concerns')
is_BlindSpot_concerns = [ 1 for i in range(len(concerns))]

for r in range(0,len(frameworks)):
    for c in range(0,len(concerns)): 
        if frameworksAndConcerns[r][c] == 1:
            is_BlindSpot_concerns[c] = 0
           
                     
for c in range(0,len(is_BlindSpot_concerns)):        
        if is_BlindSpot_concerns[c] == 1:
           Frameworks_Concerns.write(len(frameworks)+2,c+1,'BlindSpot') 
 

# Blind spot: No frames link for a Framework 
Frameworks_Concerns.write(len(frameworks)+2,0, 'Blind Spot Frameworks')   
is_BlindSpot_frameworks = [ 1 for i in range(len(frameworks))]

for r in range(0,len(frameworks)):
    for c in range(0,len(concerns)): 
        if frameworksAndConcerns[r][c] == 1:
            is_BlindSpot_frameworks[r] = 0
           
        
             
for f in range(0,len(is_BlindSpot_frameworks)):        
        if is_BlindSpot_frameworks[f] == 1:
           Frameworks_Concerns.write(f+1, len(concerns)+2,'BlindSpot') 
                       

# rows = len(frameworksAndConcerns)   
# cols = len(list(zip(*frameworksAndConcerns))):    
# read cell value -> Frameworks_Concerns.cell(0,j).value
            
   
   
from itertools import combinations 
  
# Get all combinations of frameworks[] 
# and length 2 
comb = combinations(frameworks, 2) 
r=1  
# Print the obtained combinations 
for i in list(comb):
    FW1_FW2.write(r,0,i) 
    r=r+1

FW1_FW2.write(0,1,'Intersection_of_concerns')
FW1_FW2.write(0,2,'Union_of_concerns')     
comblen = 1
unioncount = 0 
intersectioncount = 0
    
for r in range(0,len(frameworks)):
    for k in range(r+1,len(frameworks)):
        for c in range(0,len(concerns)):
            if (frameworksAndConcerns[r][c] == 1 and frameworksAndConcerns[k][c] == 1):
               intersectioncount = intersectioncount + 1
               unioncount = unioncount + 1 
            elif (frameworksAndConcerns[r][c] == 1 or frameworksAndConcerns[k][c] == 1):
                unioncount = unioncount + 1  
            else:
                pass
        FW1_FW2.write(comblen,1,intersectioncount)
        FW1_FW2.write(comblen,2,unioncount)
        comblen = comblen +1
        intersectioncount = 0
        unioncount = 0  
     
    
# Query all Classifications
print("")
print("Query for Classifications:")
results = s.query("PREFIX sto: <https://w3id.org/i40/sto#> Select distinct ?cl where {?cl a sto:StandardClassification}")

classifications = []
for row in results :
    classifications.append(sparql.unpack_row(row)[0])
    print(sparql.unpack_row(row)[0]);


# Query all concerns for each classification

classificationsAndConcerns = [[ 0 for i in range(len(concerns))] for j in range(len(classifications)) ]
for cl in classifications :
    print("")
    print("Query Concerns for Classification " + cl)
    results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {<" + cl + "> sto_iot:frames ?concern }")    #sto:Classification sto:frames sto:Concern
    
    cl_index = classifications.index(cl)
    Classifications_Concerns.write(cl_index+1,0, cl)

     

    for row in results :
        try:
            concern_index = concerns.index(sparql.unpack_row(row)[0])
            classificationsAndConcerns[cl_index][concern_index] = 1
            Classifications_Concerns.write(cl_index+1,concern_index+1, ' 1')
        except ValueError, error:
            print(error)
            


wb.save('xlwt example.xls')
print(classificationsAndConcerns)


  
# create a 2 dimensional array of concern ierarchy
print("")
print("\nQuery Concern Hierarchy:\n")

SupportingConcerns = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  Select  ?concern1  ?concern2   where {{?concern1 sto_iot:supports ?concern2} UNION {?concern1 skos:narrower ?concern2}}") 


arr = [[] for i in range(2)]
arr_Org =[]
arr_New =[]


for row in SupportingConcerns :
    arr[0].append(sparql.unpack_row(row)[0])
    arr[1].append(sparql.unpack_row(row)[1])
    
for i in range (0, len(arr[0])) :
    arr_temp = [arr[0][i],arr[1][i]]
    arr_Org.append(arr_temp)
    arr_New.append(arr_temp)
   

def hierarchy(arr_New,itr):
    arr_New1 =[]
    for i in range (0,len(arr_New)):
        rootfun = 1 
        
        for j in range (0,len(arr_Org)):
        
            #print('i='+str(i)+'j='+str(j))
            if arr_New[i][itr] == arr_Org[j][0]:
                rootfun = 0
                arr_temp=arr_New[i][:] #copy all elements of list
                arr_temp.append(arr_Org[j][1])
                #print(arr_temp) 
                arr_New1.append(arr_temp)
            
        if rootfun == 1:       
            arr_temp=arr_New[i][:]
            arr_temp.append('root')
            arr_New1.append(arr_temp)
            
    return(arr_New1)           

#iterate if root node not reached for some
for itr in range (1,16):
    #print(itr)
    enditr=True
    for r in range (0, len(arr_New) ) :
        if arr_New[r][len(arr_New[r])-1] != 'root':
            enditr=False
            break
            
    if enditr == False:
        arr_New = hierarchy(arr_New,itr)
    else:
        print('Root node reached for all leaves ')
        break
        
#print final result: path from every leaf to it's root 
for i in range (0, len(arr_New)) :
    print(str(i))
    print(arr_New[i])
       
# UNION {?concern1 skos:broader ?concern2}

#TODO: FW -> CL -> Concern
