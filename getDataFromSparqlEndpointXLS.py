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
FW1_FW2 = wb.add_sheet('FW1_FW2_Overlap',cell_overwrite_ok=True)
Concern_Hierarchy = wb.add_sheet('Concern_Hierarchy')
Frameworks_Covers_Concerns = wb.add_sheet('Frameworks_Covers_Concerns',cell_overwrite_ok=True)
classifications_Covers_Concerns = wb.add_sheet('classifications_Covers_Concerns',cell_overwrite_ok=True)

#SPARQL endpoint
s = sparql.Service('https://dydra.com/mtasnim/stoviz/sparql', "utf-8", "GET") ;


# Query all concerns
print("\nQuery for Concerns:\n")
results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {?concern a sto_iot:Concern}") ;

concerns = []
i = 0;
for row in results :
    
    concerns.append(sparql.unpack_row(row)[0])
    concern_index = concerns.index(sparql.unpack_row(row)[0])
    Frameworks_Concerns.write(0,concern_index+1, sparql.unpack_row(row)[0].replace('https://w3id.org/i40/sto#', ''))
    Classifications_Concerns.write(0,concern_index+1, sparql.unpack_row(row)[0].replace('https://w3id.org/i40/sto#', ''))
   
    
# Query all frameworks 
print("\nQuery for Frameworks:\n")
results = s.query("PREFIX sto: <https://w3id.org/i40/sto#> Select distinct ?framework where {?framework a sto:StandardizationFramework}") ;

frameworks = []
for row in results :
    frameworks.append(sparql.unpack_row(row)[0])
    


print("\nQuery Concerns for Frameworks \n" )
frameworksAndConcerns = [[ 0 for i in range(len(concerns))] for j in range(len(frameworks)) ]

for fw in frameworks :
     
    results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {<" + fw + "> sto_iot:frames ?concern}") ;  # sto:hasTargetConcern
    
    fw_index = frameworks.index(fw)
    # write framework URIs in column 0
    Frameworks_Concerns.write(fw_index+1,0, fw.replace('https://w3id.org/i40/sto#', '')) 
    
           
    for row in results :
        try:
            concern_index = concerns.index(sparql.unpack_row(row)[0])
            frameworksAndConcerns[fw_index][concern_index] = 1
            Frameworks_Concerns.write(fw_index+1,concern_index+1, 1)
    
        except ValueError, error:
            print(error)

print("\Inference if classifcation addresses a concern so does the respective framework to which it belongs:\n")
results = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select ?c ?f ?con where {?c sto:isDescribedin ?f. ?c rdf:type sto:StandardClassification. ?f rdf:type sto:StandardizationFramework. ?c sto_iot:frames ?con. ?con a sto_iot:Concern  }") ;
infFr = []
infCon = []
for row in results :
    infFr.append(sparql.unpack_row(row)[1])
    infCon.append(sparql.unpack_row(row)[2])
    
for f, c in zip(infFr, infCon):
    findex = frameworks.index(f)
    cindex = concerns.index(c)
    frameworksAndConcerns[findex][cindex] = 1
    Frameworks_Concerns.write(findex+1,cindex+1, 1)   

wb.save('xlwt example.xls')


print('Find blindspots for frameworks\n')  
# Blind spot: No frames link for a Framework 
Frameworks_Concerns.write(0,len(concerns)+2, 'Blind Spot Frameworks')
Frameworks_Concerns.write(0,len(concerns)+3, '#ConcernsInFramework') 
 

for r in range(0,len(frameworks)):
    count=0
    is_BlindSpot_frameworks=1
    for c in range(0,len(concerns)): 
        if frameworksAndConcerns[r][c] == 1:
            count = count + 1
            is_BlindSpot_frameworks = 0
    Frameworks_Concerns.write(r+1,len(concerns)+3,count)       
    if is_BlindSpot_frameworks == 1:
        print(frameworks[r])
        Frameworks_Concerns.write(r+1,len(concerns)+2,'BlindSpot')                 
       

# Blind spot: No frames link for a Concern 
Frameworks_Concerns.write(len(frameworks)+2,0, 'Blind Spot Concerns')
Frameworks_Concerns.write(len(frameworks)+3,0, 'Frequency Of Concerns')

for c in range(0,len(concerns)):
    is_BlindSpot_concerns = 1
    count = 0
    for r in range(0,len(frameworks)): 
        if frameworksAndConcerns[r][c] == 1:
            count=count+1
            is_BlindSpot_concerns = 0
            
    Frameworks_Concerns.write(len(frameworks)+3,c+1,count)        
    if is_BlindSpot_concerns == 1:
        Frameworks_Concerns.write(len(frameworks)+2,c+1,'BlindSpot')       
        
  
   
from itertools import combinations 
  
# Get all combinations of frameworks[] 
# and length 2 
comb = combinations(frameworks, 2) 
r=1  
# Print the obtained combinations 
 
for i in comb:
    FW1_FW2.write(r,0,i[0].replace('https://w3id.org/i40/sto#', '')+i[1].replace('https://w3id.org/i40/sto#', ' - ')) 
    r=r+1

FW1_FW2.write(0,1,'#Intersection_of_concerns')
FW1_FW2.write(0,2,'#Union_of_concerns')
FW1_FW2.write(0,3,'Overlap')     
comblen = 1

    
for r in range(0,len(frameworks)):
    
    for k in range(r+1,len(frameworks)):
        intersectioncount = 0
        unioncount = 0
        overlap = 0
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
        
        intersectioncount = float(intersectioncount)
        unioncount = float(unioncount)
        
        
        if(unioncount == 0):
            FW1_FW2.write(comblen,3, 0)
        else:
            overlap = intersectioncount/unioncount
            FW1_FW2.write(comblen,3,overlap)
            
        comblen = comblen +1
        
     
    
# Query all Classifications
print("\nQuery for Classifications:\n")
results = s.query("PREFIX sto: <https://w3id.org/i40/sto#> Select distinct ?cl where {?cl a sto:StandardClassification}")

classifications = []
for row in results :
    classifications.append(sparql.unpack_row(row)[0])


# Query all concerns for each classification
print("\nQuery Concerns for Classification \n")
classificationsAndConcerns = [[ 0 for i in range(len(concerns))] for j in range(len(classifications)) ]
for cl in classifications :
    
    results = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> Select distinct ?concern where {<" + cl + "> sto_iot:frames ?concern }")    #sto:Classification sto:frames sto:Concern
    
    cl_index = classifications.index(cl)
    Classifications_Concerns.write(cl_index+1,0, cl.replace('https://w3id.org/i40/sto#', ''))

     

    for row in results :
        try:
            concern_index = concerns.index(sparql.unpack_row(row)[0])
            classificationsAndConcerns[cl_index][concern_index] = 1
            Classifications_Concerns.write(cl_index+1,concern_index+1,  1)
        except ValueError, error:
            print(error)
            
wb.save('xlwt example.xls')

print('Find blindspots Classifications\n')  
# Blind spot: No frames link for a Framework 
Classifications_Concerns.write(0,len(concerns)+2, 'Blind Spot Classifications')
Classifications_Concerns.write(0,len(concerns)+3, '#ConcernsInClassification') 
 

for r in range(0,len(classifications)):
    count=0
    is_BlindSpot_classifications=1
    for c in range(0,len(concerns)): 
        if classificationsAndConcerns[r][c] == 1:
            count = count + 1
            is_BlindSpot_classifications = 0
    Classifications_Concerns.write(r+1,len(concerns)+3,count)       
    if is_BlindSpot_classifications == 1:
        print(classifications[r])
        Classifications_Concerns.write(r+1,len(concerns)+2,'BlindSpot')                 
       

# Blind spot: No frames link for a Concern 
Classifications_Concerns.write(len(classifications)+2,0, 'Blind Spot Concerns')
Classifications_Concerns.write(len(classifications)+3,0, 'Frequency Of Concerns')

for c in range(0,len(concerns)):
    is_BlindSpot_concerns = 1
    count = 0
    for r in range(0,len(classifications)): 
        if classificationsAndConcerns[r][c] == 1:
            count=count+1
            is_BlindSpot_concerns = 0
            
    Classifications_Concerns.write(len(classifications)+3,c+1,count)        
    if is_BlindSpot_concerns == 1:
        Classifications_Concerns.write(len(classifications)+2,c+1,'BlindSpot')       

wb.save('xlwt example.xls')
  
# create a 2 dimensional array of concern hierarchy
print("\nQuery Concern Hierarchy:\n")

SupportingConcerns = s.query("PREFIX sto_iot: <https://w3id.org/i40/sto/iot#> PREFIX skos: <http://www.w3.org/2004/02/skos/core#>  Select  ?concern1  ?concern2   where {{?concern1 sto_iot:supports ?concern2} UNION {?concern1 skos:broader ?concern2}}") 

arr = [[] for i in range(2)]
arr_Org =[]
arr_New =[]
c_Top = []

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
                        
            if arr_New[i][itr] == arr_Org[j][0]:
                rootfun = 0
                arr_temp=arr_New[i][:] #copy all elements of list
                arr_temp.append(arr_Org[j][1])
                arr_New1.append(arr_temp)
            
        if rootfun == 1:       
            arr_temp=arr_New[i][:]
            arr_temp.append('root')
            arr_New1.append(arr_temp)
            
    return(arr_New1)           

#iterate if root node not reached for some
for itr in range (1,16):
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
        


for r in range (0, len(arr_New)) :
    while(arr_New[r][len(arr_New[r])-1] == 'root'):
        arr_New[r].pop()
    
    c_Top.append(arr_New[r][len(arr_New[r])-1])
   
    
#print final result: path from every leaf to it's root 
for i in range (0, len(arr_New)) :
    for j in range (0,len(arr_New[i])):
        Concern_Hierarchy.write(i,j+1,arr_New[i][j].replace('https://w3id.org/i40/sto#', ''))
       

wb.save('xlwt example.xls')


print('\nFind top concerns\n')
c_Top = list(dict.fromkeys(c_Top))
print('')
print(str(len(c_Top))+' Top concerns:\n')  


# get subconcerns of a given concern
def getSubConcerns(Concern):
    subconcerns=[]
    for r in range (0, len(arr_New)) :
        for c in range (0, len(arr_New[r])):
            if (arr_New[r][c]) == Concern:
                while(c>=0):
                    subconcerns.append(arr_New[r][c])
                    c=c-1
            
      
    subconcerns = list(dict.fromkeys(subconcerns))
    
    
    return(subconcerns)    


# calculate specificity score
print('\nCalculate specificity scores for concerns\n')

concern_Level = [0 for i in range(len(concerns))]

for con in range (0,len(concerns)):
    for r in range (0, len(arr_New)) :
        for c in range (0,len(arr_New[r])):
        
            if(concerns[con]==arr_New[r][c]):
                if(concern_Level[con]<c):
                    concern_Level[con] = c
                   


#Dictionary containing Concerns and it's levels
Con_dict = {c:[ concern_Level[concerns.index(c)],0] for c in concerns}

   
# Specificity of concerns and of Frameworks and Classifications    
def Fspecificity (con,level):
    
    sum=0
    subconcerns = []
    if(level==0):
        return 1
    else:
        subconcerns = getSubConcerns(con)
        subconcerns.remove(con)
        for s in subconcerns:
            if s in Con_dict.keys():
                sum = sum + Fspecificity(s,Con_dict[s][0])
        specificity= 1.0/pow((0.2+sum),0.3)
        return(specificity)
        
# Specificity is 1 if its a leaf in hierarchy tree otherwise specificity= 1.0/pow((0.2+sum),0.3)


for k, v in Con_dict.items():
    v[1] = Fspecificity(k,v[0])
    

i=0  
Frameworks_Concerns.write(len(frameworks)+5,0,'specificity')
Classifications_Concerns.write(len(classifications)+5,0,'specificity') 
Frameworks_Concerns.write(0,len(concerns)+4,'specificity')
Classifications_Concerns.write(0,len(concerns)+4,'specificity') 
for k, v in Con_dict.items():
    if k in concerns:
        index = concerns.index(k)
        Frameworks_Concerns.write(len(frameworks)+5,index+1,v[1])
        Classifications_Concerns.write(len(classifications)+5,index+1,v[1])
    
    i=i+1
wb.save('xlwt example.xls') 

for f in range (0,len(frameworks)):
    sum = 0.0
    avg=0.0
    count=0
    for c in range (0,len(concerns)):
        if frameworksAndConcerns[f][c] == 1:
            count= count+1
            sum = sum + Con_dict[concerns[c]][1]
    if count==0:
        Frameworks_Concerns.write(f+1,len(concerns)+4, 0)
    else:
        avg = sum / count
        Frameworks_Concerns.write(f+1,len(concerns)+4, avg) 
        
    
    
wb.save('xlwt example.xls')    


for cl in range (0,len(classifications)):
    sum = 0.0
    avg=0.0
    count=0
    for c in range (0,len(concerns)):
        if classificationsAndConcerns[cl][c] == 1:
            count= count+1
            sum = sum + Con_dict[concerns[c]][1]
    if count==0:
        Classifications_Concerns.write(cl+1,len(concerns)+4, 0)
    else:
        avg = sum / count
        Classifications_Concerns.write(cl+1,len(concerns)+4, avg)
         
    
wb.save('xlwt example.xls') 
# Calculate coverage of a Top concern by a given Framework           

def frameCoversConcern(framework , Concern ):
    c = 0
    subconcerns=[]
    Framework_Concerns=[]
    F_C=[]
    subconcerns = getSubConcerns(Concern)
    
    #get all concerns addressed by framework
    findex = frameworks.index(framework)
    for c in range(len(concerns)):
        if(frameworksAndConcerns[findex][c] == 1):
            Framework_Concerns.append(concerns[c]) 
        else:
            pass
    c = 0
    F_C = list(dict.fromkeys(Framework_Concerns))
    for i in range (0, len(subconcerns)) :
        for j in range (0, len(F_C)):
            if (F_C[j]==subconcerns[i]):
                c = c+1
    
    c=float(c)       
    subConCount=len(subconcerns)
    subConCount=float(subConCount)
    if(subConCount!=0):
        Coverage = (c/subConCount)*100
    else:
        print('This is a leaf concern')
    return Coverage

print('\nCalculate Coverage for frameworks\n')
   
for i in frameworks :
    findex=frameworks.index(i)
    Frameworks_Covers_Concerns.write(findex+1,0,i.replace('https://w3id.org/i40/sto#', ''))
    for j in c_Top:
        cindex=c_Top.index(j)
        Frameworks_Covers_Concerns.write(0,cindex+1,j.replace('https://w3id.org/i40/sto#', ''))
        Coverage=frameCoversConcern(i , j )
        Frameworks_Covers_Concerns.write(findex+1,cindex+1,Coverage)
    
           
wb.save('xlwt example.xls')  
          
print('\nCalculate Coverage for classifications\n')

def clasfCoversConcern(classification , Concern ):
    c = 0
    subconcerns=[]
    Classification_Concerns=[]
    C_C=[]
    subconcerns = getSubConcerns(Concern)
    
    #get all concerns addressed by classification
    cindex = classifications.index(classification)
    for c in range(len(concerns)):
        if(classificationsAndConcerns[cindex][c] == 1):
            Classification_Concerns.append(concerns[c]) 
        else:
            pass
    c = 0
    C_C = list(dict.fromkeys(Classification_Concerns))
    for i in range (0, len(subconcerns)) :
        for j in range (0, len(C_C)):
            if (C_C[j]==subconcerns[i]):
                c = c+1
    
    c=float(c)       
    subConCount=len(subconcerns)
    subConCount=float(subConCount)
    if(subConCount!=0):
        Coverage = (c/subConCount)*100
    else:
        print('This is a leaf concern')
    return Coverage

for i in classifications :
    clindex=classifications.index(i)
    classifications_Covers_Concerns.write(clindex+1,0,i.replace('https://w3id.org/i40/sto#', ''))
    for j in c_Top:
        conindex=c_Top.index(j)
        classifications_Covers_Concerns.write(0,conindex+1,j.replace('https://w3id.org/i40/sto#', ''))
        Coverage=clasfCoversConcern(i , j )
        classifications_Covers_Concerns.write(clindex+1,conindex+1, Coverage)
         
    
wb.save('xlwt example.xls')   
# UNION {?concern1 skos:broader ?concern2}

#TODO: FW -> CL -> Concern
