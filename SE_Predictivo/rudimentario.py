#################################################################################
#####-----------------------------------------------------------------------#####
####-------------------------------------------------------------------------####
###------------------------SISTEMA EXPERTO PREDICTIVO ------------------------###
##-----------------------------------------------------------------------------##
#-------------------------------------------------------------------------------#

import csv
import random 


#-------------------------------------------------------------------------------#

objetos = []
with open('objeto.csv', 'r') as File:
	fieldnames = ['ID_OBJECT', 'NAME']
	reader = csv.DictReader(File, fieldnames= fieldnames, delimiter=';')
	for row in reader:
		objetos.append(row)


#--------------------------------------------------------------------------------#
atributos = []
with open('atributo.csv', 'r') as File:
	fieldnames = ['ID_ATTRIB', 'NAME']
	reader = csv.DictReader(File, fieldnames= fieldnames, delimiter=';')
	for row in reader:
		atributos.append(row)
	
#--------------------------------------------------------------------------------#

relaciones = []
with open('relacion.csv', 'r') as File:
	fieldnames = ['ID_OBJECT', 'ID_ATTRIB']
	reader = csv.DictReader(File, fieldnames= fieldnames, delimiter=';')
	for row in reader:
		relaciones.append(row)
		



##-------------------------La agenda comienza "vacía" ----------------------------#
Agenda = []

##---------------------Funcion encargada de rellenar la agenda con los objetos que cumplen la categoría --------------------------------##
def schedule_init(objetos,  relaciones, category):

	clave = ''
	value = 0
	for dict in relaciones:
		if(dict != relaciones[0] and dict.get('ID_ATTRIB') == category.get('ID_ATTRIB')):
			clave = dict.get('ID_OBJECT')
			value = 0
			candidate = {'ID_OBJECT' : clave, 'VALUE' : value  }
			Agenda.append(candidate)
			 

###--------------------------Devuelve una categoría que esté relacionada al candidato-----------------------###
def make_category(relaciones, atributos, last_category):
	new = {'ID_ATTRIB': '', 'NAME': ''}
	candidate = Agenda[0]
	id_object = candidate.get('ID_OBJECT')
	for attrib in atributos:
		if(attrib.get('ID_ATTRIB') != last_category.get('ID_ATTRIB')):
			candidate_rel = {'ID_OBJECT': id_object, 'ID_ATTRIB': attrib.get('ID_ATTRIB')}
			if(candidate_rel in relaciones):
				new['ID_ATTRIB'] = attrib.get('ID_ATTRIB')
				new['NAME'] =attrib.get('NAME')
				return new
		

	return new


###-------------------Recibe objeto de la agenda y lo coloca en la primera posicion de la Agenda------------###
def put_in_top(object):
	index_object = Agenda.index(object)
	first_object = Agenda[0]
	Agenda[0] = object
	Agenda[index_object] = first_object
	value = int(object.get('VALUE'))
	value += 1
	object['VALUE'] = value


### ----Aumenta en 1 el 'VALUE' de los objetos candidatos en la agenda, si estos tienen en la tabla relaciones el atributo 'category'
def check_schedule(relaciones, category):
	for object in Agenda:
		id_object = object.get('ID_OBJECT')
		id_attrib = category.get('ID_ATTRIB')
		candidate = {'ID_OBJECT': id_object, 'ID_ATTRIB': id_attrib}
		if(candidate in relaciones):
			put_in_top(object)    #pone el objeto en el primer lugar de la Agenda


#----------------- Si la agenda está vacía, entonces, se inicializa ---------------#
def agenda(objetos, atributos, relaciones, category, last_category):
	new_category = {'ID_ATTRIB': '', 'NAME': ''}
	if (len(Agenda) == 0):
		schedule_init(objetos, relaciones, category) #inicializa laa agenda 
	
	new_category = make_category(relaciones, atributos, last_category)		
	return new_category

##---------------------------------------------------------------------##
def Random_category():
	rand_index = random.randint(1, len(atributos) - 1)
	return rand_index


##---------Se elimina una categoría si ésta ya se usó------ ##

def  delete_category(category, atributos):
	if(category in atributos):
		del_index = atributos.index(category)
		del(atributos[del_index])

##---------Se eliminan los objetos dependiendo si tienen o no alguna categoría relacionada -------##
def fix_agenda(relaciones, category, user_input):
	if (user_input == 'N' or user_input == 'n'):
		delete_category(category, atributos)
		for object in Agenda:
			id_object = object.get('ID_OBJECT')
			id_attrib = category.get('ID_ATTRIB')
			candidate = {'ID_OBJECT': id_object, 'ID_ATTRIB': id_attrib}
			if(candidate in relaciones):			
				index = Agenda.index(object)
				del(Agenda[index])

	else:
		if(user_input == 'S' or user_input == 's'):
			check_schedule(relaciones, category)
			delete_category(category, atributos)
			for object in Agenda:
				id_object = object.get('ID_OBJECT')
				id_attrib = category.get('ID_ATTRIB')
				candidate = {'ID_OBJECT': id_object, 'ID_ATTRIB': id_attrib}
				if(candidate in relaciones):
					pass
				else:
					index = Agenda.index(object)
					del(Agenda[index])

				

###------------------------Se busca el animal al que corresponde el ID -------------##

def show_answer(objetos):
	for object in objetos:
		if(object.get('ID_OBJECT') == Agenda[0].get('ID_OBJECT')):
			return object.get('NAME')

#////////////////////7//-----------FUNCION PRINCIPAL-----------////////////////////////# 

def interface(objetos, atributos, relaciones):

	random_index = Random_category()
	category = { 'ID_ATTRIB': atributos[random_index].get('ID_ATTRIB'),	'NAME' : atributos[random_index].get('NAME') }
	category_name = category.get('NAME')
	adivinado = 0

	print('Es un {0} ? :'.format(category_name))
	user_input = input(" 'S' para Sí 'N' para no: ")
	if (user_input == 'S' or user_input == 's'):

		delete_category(category, atributos)
		while (adivinado == 0 or len(Agenda) == 0):
			last_category = category
			category = agenda(objetos, atributos, relaciones, category, last_category) ## agenda escoge categoría
			category_name = category.get('NAME')
			if (category_name != ''):
				print('Es {}?: '.format(category_name))
				user_input = input(" 'S' para Sí 'N' para no: ")
				fix_agenda(relaciones, category, user_input)
			else:
				respuesta = show_answer(objetos)
				print('ES {}'.format(respuesta))
				adivinado = 1


	else:
		delete_category(category, atributos)
		interface(objetos, atributos, relaciones)	





interface(objetos, atributos, relaciones)


