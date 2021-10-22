# enfermedades = faringitis, gripa
# síntomas : dolor_garganta, fiebre, malestar, tos


def S_difuso():
	enfermedades = ['faringitis', 'gripa']
	sintomas = ['dolor_garganta', 'fiebre', 'malestar', 'tos']

	pause = 0
	faringitis  =  0
	gripa = 0
	sintoma = input('Sintoma: ')
	while pause == 0:
		sintoma = input('Sintoma: ')
		r1 = True if (sintoma == sintomas[1]) else False
		r2 = True if (sintoma == sintomas[3]) else False
		r3 = True if (sintoma == sintomas[0]) else False
		r4 = True if (sintoma == sintomas[3]) else False

		if ( r1 or r2):
			 if (gripa == 0):
			 	gripa = gripa + 0.2 if(r1) else gripa + 0.7 
			 else:
			 	gripa = gripa + (1 - gripa)*0.2  if (r2) else gripa + (1 - gripa)*0.7
		else:
			if ( r3 or r4):
			 	if (faringitis == 0):
			 		faringitis = faringitis + 0.8 if(r3) else faringitis + 0.6
			 	else:
			 		faringitis = faringitis + (1 - faringitis)*0.8  if (r3) else faringitis + (1 - faringitis)*0.6
		print('Terminar: 1 \n continuar : 0')
		pause = int(input())
	if(faringitis > gripa):
		print('Usted tiene Faringitis en un {0}%'.format(faringitis))
	else:
		print('Usted tiene Gripa en un {0}%'.format(gripa))



S_difuso()
