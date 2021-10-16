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
	fieldnames = ['ID_RELATION', 'ID_OBJECT', 'ID_ATTRIB']
	reader = csv.DictReader(File, fieldnames= fieldnames, delimiter=';')
	for row in reader:
		relaciones.append(row)


###-----------------------------------------------------------------###
relations_copy = relaciones
attribs_copy = atributos

###-----------------------------------------------------------------###

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
			 

##--- La agenda puede guardar los ID's de los objetos como keys y la puntuacion como values

def make_category(relaciones, attribs_copy):
	new = {'ID_ATTRIB': '', 'NAME': ''}
	candidate = Agenda[0]
	for relation in relaciones:
		if (relation != relaciones[0] and relation.get('ID_OBJECT') == candidate.get('ID_OBJECT') ):
			for attrib in atributos:
				if (relation.get('ID_ATTRIB') == attrib.get('ID_ATTRIB')):
					new = {'ID_ATTRIB': relation.get('ID_ATTRIB'), 'NAME': attrib.get('NAME')}
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
		for relation in relaciones:
			if (relation != relaciones[0] and relation.get('ID_OBJECT') == object.get('ID_OBJECT')):
				if(relation.get('ID_ATTRIB') == category.get('ID_ATTRIB')):
					put_in_top(object)    #pone el objeto en el primer lugar de la Agenda
					break


#----------------- Si la agenda está vacía, entonces, se inicializa ---------------#
def agenda(objetos, attribs_copy, relaciones, category):
	new_category = {'ID_ATTRIB': '', 'NAME': ''}
	if (len(Agenda) == 0):
		schedule_init(objetos, relaciones, category) #inicializa laa agenda 
		new_category = make_category(relaciones, attribs_copy)

	else:	
		new_category = make_category(relaciones, attribs_copy)
		
	return new_category

##---------------------------------------------------------------------##
def Random_category():
	rand_index = random.randint(1, len(attribs_copy) - 1)
	return rand_index


##---------Se elimina una categoría si ésta ya se usó------ ##

def  delete_category(category, attribs_copy):
	if(category in attribs_copy):
		del_index = attribs_copy.index(category)
		del(attribs_copy[del_index])

##---------Se eliminan los objetos dependiendo si tienen o no alguna categoría relacionada -------##
def delete_in_agenda(relaciones, category, user_input):
	if (user_input == 'N' or user_input == 'n'):
		delete_category(category, attribs_copy)
		for object in Agenda:
			for relation in relaciones:
				if (relation != relaciones[0] and object.get('ID_OBJECT') == relation.get('ID_OBJECT')):
					if (relation.get('ID_ATTRIB') == category.get('ID_ATTRIB')):
						index = Agenda.index(object)
						del(Agenda[index])
						break

	else:
		boolean = 0
		if(user_input == 'S' or user_input == 's'):
			for object in Agenda:
				for relation in relaciones:
					if(relation != relaciones[0] and  object.get('ID_OBJECT') == relation.get('ID_OBJECT')):
						if (relation.get('ID_ATTRIB') == category.get('ID_ATTRIB')):
							bolean = 1 
							break
				if (boolean == 0):
					index = Agenda.index(object)
					del(Agenda[index])	


###------------------------Se busca el animal al que corresponde el ID -------------##

def show_answer(objetos):
	for object in objetos:
		if(object.get('ID_OBJECT') == Agenda[0].get('ID_OBJECT')):
			return object.get('NAME')

#////////////////////7//-----------FUNCION PRINCIPAL-----------////////////////////////# 

def interface(objetos, attribs_copy, relaciones):

	random_index = Random_category()
	category = { 'ID_ATTRIB': attribs_copy[random_index].get('ID_ATTRIB'),	'NAME' : attribs_copy[random_index].get('NAME') }
	category_name = category.get('NAME')
	adivinado = 0

	print('Es un {0} ? :'.format(category_name))
	user_input = input(" 'S' para Sí 'N' para no: ")
	if (user_input == 'S' or user_input == 's'):

		delete_category(category, attribs_copy)
		while (adivinado == 0 or len(Agenda) == 0):
			category = agenda(objetos, attribs_copy, relaciones, category) ## agenda escoge categoría
			category_name = category.get('NAME')
			if(category_name != ''):
				print('Es {0}?'.format(category_name))
				user_input = input(" 'S' para Sí 'N' para no: ")
			if(user_input == 's' or user_input =='S' or category_name == ''):
				check_schedule(relaciones, category)
				delete_category(category, attribs_copy)
				if (len(Agenda) == 2 ):
					if (Agenda[0].get('VALUE') > Agenda[1].get('VALUE')):
						respuesta = show_answer(objetos)
						print('Es {0}'.format(respuesta))
						adivinado = 1

			delete_in_agenda(relaciones, category, user_input)
	else:
		delete_category(category, attribs_copy)
		interface(objetos, attribs_copy, relaciones)	




interface(objetos, attribs_copy, relaciones)


