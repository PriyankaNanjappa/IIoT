import sparql
# Writing to an excel  
# sheet using Python
import xlwt 
from xlwt import Workbook 
#from xlwt import Cell

# Workbook is created 
wb = Workbook() 
  
# add_sheet is used to create sheets. 
statistics = wb.add_sheet('statistics',cell_overwrite_ok=True)

#SPARQL endpoint
s = sparql.Service('https://dydra.com/pnanjappa/thesis/sparql', "utf-8", "GET") ;

statistics.write(0,0, 'Measure')
statistics.write(0,1, 'Value')

print("\nQuery for number of classes:\n")
results1 = s.query(" Select distinct ?clas where {?clas rdf:type owl:Class}") ;
statistics.write(1,0, 'Classes')
c1=0
for row in results1 :
    print(c1)
    print(sparql.unpack_row(row)[0])
    c1=c1+1
   # print(sparql.unpack_row(row)[1])
statistics.write(1,1, c1)

print("\nQuery for number of Triples:\n")
results2 = s.query(" Select (count(?s) as ?count) where {?s ?p ?o}") ;
statistics.write(2,0, 'Triples')
for row in results2 :
    print(sparql.unpack_row(row)[0])
    #print(sparql.unpack_row(row)[1])
    statistics.write(2,1, sparql.unpack_row(row)[0])
    
print("\nQuery for number of Predicates:\n")  
results4 = s.query(" Select ?p (count(?p) as ?pcount) where {?s ?p ?o} Group by ?p") ;
statistics.write(4,0, 'Predicates')
c4=0
for row in results4 :
    c4=c4+1
    print(sparql.unpack_row(row)[0])
    print(sparql.unpack_row(row)[1])
    
statistics.write(4,1, c4)    
wb.save('keystatistics.xls')

print("\nQuery for number of Instances:\n")  
results5 = s.query(" select  ?instance ?class  where {?instance a ?class . ?class a owl:Class} Group by ?instance") ;
# (count(?instance) as ?pcount) count says how many classes the instance belongs to.
statistics.write(5,0, 'Instances')
c5=0
for row in results5 :
    c5=c5+1
    print(sparql.unpack_row(row)[0])
    print(sparql.unpack_row(row)[1]) 
    
statistics.write(5,1, c5)

statistics.write(6,0, 'Instances per class')
c6=0
c5=float(c5)
c1=float(c1)
c6=c5/c1
statistics.write(6,1, c6)


# print("\nQuery for number of Entities:\n")  
# results = s.query(" select  ?entities (count(?entities) as ?ecount) where {?entities ?p ?o . ?entities a owl:Thing } Group by ?entities") ;
# statistics.write(6,0, 'Entities')
# c=0
# for row in results :
    # c=c+1
    # print(sparql.unpack_row(row)[0])
    # print(sparql.unpack_row(row)[1])
    
# statistics.write(6,1, c)    
# wb.save('keystatistics.xls')

print("\nQuery for number of Subjects:\n") 
results3 = s.query(" Select distinct ?s where {?s ?p ?o} ") ;
statistics.write(3,0, 'Subjects')
c3=0
for row in results3 :
    c3=c3+1
    print(sparql.unpack_row(row)[0])
   # print(sparql.unpack_row(row)[1])
    
statistics.write(3,1, c3)    
wb.save('keystatistics.xls')
 
print("\nQuery for number of blank nodes:\n") 
results3 = s.query(" Select (count(distinct ?o) as ?classes) where {?s ?p ?o. FILTER isBlank(?o) } ") ;
statistics.write(7,0, 'blank nodes')
c7=0
for row in results3 :
    
    print(sparql.unpack_row(row)[0])
   # print(sparql.unpack_row(row)[1])
    
statistics.write(7,1, sparql.unpack_row(row)[0])    
wb.save('keystatistics.xls')

print("\nQuery for Syntactic validity of literals\n") 
results3 = s.query(" Select (count(distinct ?o) as ?obj) where {?s ?p ?o.  FILTER isLiteral(?o)} ") ;
statistics.write(8,0, 'literals')
c8=0
for row in results3 :
    
    print(sparql.unpack_row(row)[0])
   # print(sparql.unpack_row(row)[1])
    
statistics.write(8,1, sparql.unpack_row(row)[0])    
wb.save('keystatistics.xls')


print("\nQuery for IRIs\n") 
results3 = s.query(" Select (count(distinct ?o) as ?obj) where {?s ?p ?o.  FILTER isIRI(?o)} ") ;
statistics.write(9,0, 'IRIs')
c9=0
for row in results3 :
    
    print(sparql.unpack_row(row)[0])
   # print(sparql.unpack_row(row)[1])
    
statistics.write(9,1, sparql.unpack_row(row)[0])    
wb.save('keystatistics.xls')

print("\nQuery for Unique Objects\n") 
results3 = s.query(" Select (count(distinct ?o) as ?obj) where {?s ?p ?o} ") ;
statistics.write(10,0, 'Objects')
c10=0
for row in results3 :
    
    print(sparql.unpack_row(row)[0])
   # print(sparql.unpack_row(row)[1])
    
statistics.write(10,1, sparql.unpack_row(row)[0])    
wb.save('keystatistics.xls')

print("\nDate datatype\n") 
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasPublicationDate ?o. ?s rdf:type sto:Standard  } ") ;
c11=0
for row in results3 :
    c11=c11+1

   # print(sparql.unpack_row(row)[1])
print('\n ')
print(c11)   
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasPublicationDate ?o. ?s rdf:type sto:Standard . FILTER ( datatype(?o) = xsd:date )} ") ;
c12=0
for row in results3 :
    c12=c12+1

print('\n ')
print(c12)  
c11 = float(c11)
c12 = float(c12) 
frac = c12/c11
statistics.write(11,0, 'DateLiteralForsto:hasPublicationDate')
statistics.write(11,1, c12) 
statistics.write(11,2, c11) 
statistics.write(11,3, frac) 

##########################################
print("\nanyURI datatype\n") 
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasOfficialResource ?o  } ") ;
c11=0
for row in results3 :
    c11=c11+1

# print(sparql.unpack_row(row)[1])
print('\n ')
print(c11)   
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasOfficialResource ?o. FILTER ( datatype(?o) = xsd:anyURI )} ") ;
c12=0
for row in results3 :
    c12=c12+1

print('\n ')
print(c12)  
c11 = float(c11)
c12 = float(c12) 
frac = c12/c11
statistics.write(12,0, 'anyURILiteralForsto:hasOfficialResource')
statistics.write(12,1, c12)
statistics.write(12,2, c11)
statistics.write(12,3, frac)    
#############################################
print("\string datatype\n") 
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s rdfs:label ?o  } ") ;
c11=0
for row in results3 :
    c11=c11+1

# print(sparql.unpack_row(row)[1])
print('\n ')
print(c11)   
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s rdfs:label ?o. FILTER ( datatype(?o) = xsd:string )} ") ;
c12=0
for row in results3 :
    c12=c12+1

print('\n ')
print(c12)  
c11 = float(c11)
c12 = float(c12) 
frac = c12/c11
statistics.write(13,0, 'StringLiteralForrdfs:label')
statistics.write(13,1, c12)
statistics.write(13,2, c11)
statistics.write(13,3, frac) 
wb.save('keystatistics.xls')
###############################################
print("\anyURI datatype for sto:hasWikipediaArticle\n") 
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasWikipediaArticle ?o  } ") ;
c11=0
for row in results3 :
    c11=c11+1

# print(sparql.unpack_row(row)[1])
print('\n ')
print(c11)   
results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasWikipediaArticle ?o. FILTER ( datatype(?o) = xsd:anyURI )} ") ;
c12=0
for row in results3 :
    c12=c12+1

print('\n ')
print(c12)  
c11 = float(c11)
c12 = float(c12) 
frac = c12/c11
statistics.write(14,0, 'anyURILiteralFor sto:hasWikipediaArticle')
statistics.write(14,1, c12)
statistics.write(14,2, c11)
statistics.write(14,3, frac) 
wb.save('keystatistics.xls')
#####################################################

# print("\valid dates for sto:hasPublicationDate\n") 
# results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where {?s sto:hasPublicationDate ?o. FILTER ( datatype(?o) = xsd:date )   } ") ;
# c11=0
# for row in results3 :
    # c11=c11+1

   # # print(sparql.unpack_row(row)[1])
# print('\n ')
# print(c11)   
# results3 = s.query("PREFIX sto: <https://w3id.org/i40/sto#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>  Select distinct ?s  where { SERVICE SILENT <https://dydra.com/mtasnim/stoviz/sparql> {?s sto:hasPublicationDate ?o.}  FILTER ( ?o < "11-11-2019"^^xsd:date)} ") ;
# c12=0
# for row in results3 :
    # c12=c12+1

# print('\n ')
# print(c12)  
# c11 = float(c11)
# c12 = float(c12) 
# frac = c12/c11
# statistics.write(15,0, 'Valid dates for sto:hasPublicationDate')
# statistics.write(15,1, c12) 
# statistics.write(15,2, c11) 
# statistics.write(15,3, frac) 
# #################################################################### 
wb.save('keystatistics.xls')