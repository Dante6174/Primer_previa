import csv



### -------LEER UN ARCHIVO .CSV CON csv.reader()---------###
''' 
with open('ejemplo.csv') as File:
    reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        print(row)

'''


### -------LEER UN ARCHIVO .CSV CON Dict.Reader()---------###


results =[]
with open('atributo.csv', 'r') as File:
	fieldnames = ['ID_OBJET', 'NAME']
	reader = csv.DictReader(File, fieldnames= fieldnames, delimiter=';')
	for row in reader:
		results.append(row)
		print(row)



	
