def sistema_experto_basico():
  pause = int(input("Desea utilizar el sistema experto? SI = 0 NO = 1: "))
  sintomas_gripa = ["fiebre","tos","malestar"]
  sintomas_faringitis = ["dolor_garganta","malestar"]
  faringitis=0
  gripa=0
  while(pause == 0):
    a = input("Que sintoma tiene?: ")
    if(a in sintomas_gripa and a in sintomas_faringitis):
      gripa +=1
      faringitis +=1 
    elif(a in sintomas_faringitis):
      faringitis +=1
    elif(a in sintomas_gripa):
      gripa +=1
    else:
        print('Entrada no permitida')
        
    pause = int(input("Para continuar ingresando síntomas presione  SI =0, Salir  NO = 1: ")) 

  if(gripa > faringitis):
    print("tiene gripa")
  elif(faringitis > gripa):
    print("tiene faringitis")  
  else:
    print("no se puede identificar el sintoma")

sistema_experto_basico()