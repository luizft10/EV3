
#!/usr/bin/env python3
from time import sleep
from classe import Robot

r = Robot('B', 'A', 'C', '2', '1', '3', '4', 7, 2.7, 13.5)
cores = ['unknown','black','blue','green','yellow','red','white','brown']
# [cores[r.sensorE.value()], cores[r.sensorD.value()]]
# r.sensorE.mode = "COL-AMBIENT"
# r.sensorD.mode = "COL-AMBIENT"
# r.direcoes = []
# r.cores = []
# r.coresAprendidas = {4: -90, 3:0, 5:90}
# teste = False
#while True:

	# r.girar(90)
	# sleep(2)
	# r.girar(-90)
	# sleep(5)
	# r.girarRoda(90)
	# r.andarTempo(-200,-200,200, True)


#r.girarRoda(90)
r.girar(360)
# e = 0
# d = 0
# while True:

# r.bateParede()
	# i = 0
	# d = 0
	# e = 0
	# seguidos = 0
	# bol = True
	# for i in range(200):

	# 	##############
	# 	#   RAMPA    #
	# 	##############
	# 	print("SpeedTop", r.motorD.speed_sp, r.motorE.speed_sp)
	# 	r.andarTempo(400, 400, 100)
	# 	if (r.motorE.speed < 380) and i > 10:
	# 		e += 1
	# 		bol = False
	# 	if (r.motorD.speed < 380) and i > 10:
	# 		d += 1
	# 		bol = False

	# 	if bol:
	# 		e = 0
	# 		d = 0

	# 	if e > 3:
	# 		r.andarTempo(-200,-200, 600, True)
	# 		r.andarTempo(-300, 0, 400, True)
	# 		r.andarTempo(200, 200, 600, True)
	# 		break
	# 	if d > 3:
	# 		r.andarTempo(-200,-200, 600, True)
	# 		r.andarTempo(0, -300, 400, True)
	# 		r.andarTempo(200, 200, 600, True)
	# 		break

	# 	bol = True

	# for i in range(200):
	# 	r.andarRotacao(100, -100, 300)
	# 	e += r.motorE.speed
	# 	d += r.motorD.speed
	# 	print(r.motorE.speed, r.motorD.speed)
	# r.stop()
	# print("Media", e/200, d/200)
	# e = 0
	# d = 0
	# sleep(5)
	# for k in range(200):
	# 	r.andarRotacao(-100, 100, 300)
	# 	e += r.motorE.speed
	# 	d += r.motorD.speed
	# 	print(r.motorE.speed, r.motorD.speed)
	# r.stop()
	# print("Media", e/200, d/200)
	# e = 0
	# d = 0
	# sleep(5)
	# print(C)
	# r.girar(-90)
	# sleep(2)
	# r.girar(90)
	# sleep(4)
	# C += 0.1
	# r.razao = r.odometria(C, c)


	# if r.sensorE.value() not in [0, 1, 6, 7]:
	# 	if not teste:
	# 		while not r.alinhaCor([r.sensorE.value()], 6, r.sensorE, r.sensorD, 200, 0, True):
	# 			continue
	# 		# r.andarTempo(400, 400, 200, True)

	# 	if r.corAtual not in [int(key) for key in r.coresAprendidas.keys()]:
	# 		print("deadEnd")
	# 	else:
	# 		if r.corAtual == 3:
	# 			if r.verificaEntradaPraca():
	# 				r.mapeamento = False
	# 				print("Entra Praca e o cacete")
	# 				r.andarTempo(400,400, 600, True)
	# 				r.girar(180)
	# 				r.voltaPraca()
	# 			else:
	# 				direcao = r.coresAprendidas[r.corAtual]
	# 				r.girar(direcao)
	# 				r.saindoCor()
	# 		else:
	# 			direcao = r.coresAprendidas[r.corAtual]
	# 			r.girar(direcao)
	# 			r.saindoCor()	 		
		

	# if r.sensorD.value() not in [0, 1, 6, 7]:
	# 	if not teste:
	# 		while not r.alinhaCor([r.sensorD.value()], 6, r.sensorD, r.sensorE, 0, 200, True):
	# 			continue
	# 		# r.andarTempo(400, 400, 200, True)

	# 	if r.corAtual not in [int(key) for key in r.coresAprendidas.keys()]:
	# 		print("deadEnd")
	# 	else:
	# 		if r.corAtual == 3:
	# 			if r.verificaEntradaPraca():
	# 				r.mapeamento = False
	# 				print("Entra Praca eo cacete")
	# 				r.andarTempo(400,400, 600, True)
	# 				r.girar(180)
	# 				r.voltaPraca()
	# 			else:
	# 				direcao = r.coresAprendidas[r.corAtual]
	# 				r.girar(direcao)
	# 				r.saindoCor()
	# 		else:
	# 			direcao = r.coresAprendidas[r.corAtual]
	# 			r.girar(direcao)
	# 			r.saindoCor()





	####################
	# ALINHA COR PRETO #
	####################
	# r.andarTempo(200,200,100)

	# if not garraOcupada:
	# 	if r.sensorE.value() in [0,1,7]:
	# 		while not r.alinhaCor([0,1,7], 6, r.sensorE, r.sensorD, 100, 0, False, True):
	# 			continue
	# 	if r.sensorD.value() in [0,1,7]:
	# 		while not r.alinhaCor([0,1,7], 6, r.sensorD, r.sensorE, 0, 100, False, True):
	# 			continue

	# 	r.garraOcupada = True




	################
	# LUMINOSIDADE #
	################
	# print(r.sensorD.value() , " - ", r.sensorE.value())	
	# sleep(2)





	# r.andarTempo(400, 400, 100)
	###########
	# APRENDE #
	###########
	# r.andarTempo(300, 300, 100)
	# r.saindoPista()
	# print(r.corAtual)
	# if r.sensorE.value() not in [0, 1, 7, 6]:
	# 	print(cores[r.sensorE.value()], cores[r.sensorD.value()])		
	# 	while not r.alinhaCor(r.sensorE.value(), r.sensorE, r.sensorD, 100, 0, True):
	# 		continue	
	# 	print(r.corAtual)

	# if r.sensorD.value() not in [0, 1, 7, 6]:
	# 	print(cores[r.sensorE.value()], cores[r.sensorD.value()])
	# 	while not r.alinhaCor(r.sensorD.value(), r.sensorD, r.sensorE, 0, 100, True):
	# 		continue
	# 	print(r.corAtual)




	################
	# INPUT SENSOR #
	################
	# tempRgb = [r.sensorM.value(0), r.sensorM.value(1), r.sensorM.value(2)]
	# tempHsv = r.convertHSV(tempRgb)
	# hsv = list(tempHsv)
	# hsv[2] = 100	
	# rgb = r.convertRGB(hsv)

	# print("temp RGB:", tempRgb, "temp HSV:",tempHsv, "HSV:",hsv, "Cor Lida:", r.readColor(rgb))
	# sleep(2)






	##############
	# ALINHA COR #
	##############
	# r.andarTempo(300, 300, 100)
	# r.saindoPista()
	# # print(cores[r.sensorE.value()], cores[r.sensorD.value()])	
	# if r.sensorE.value() not in [0, 1, 7, 6]:
	# 	print(cores[r.sensorE.value()], cores[r.sensorD.value()])		
	# 	while not r.alinhaCor([r.sensorE.value()], 6, r.sensorE, r.sensorD, 80, 0):
	# 		continue

	# if r.sensorD.value() not in [0, 1, 7, 6]:
	# 	print(cores[r.sensorE.value()], cores[r.sensorD.value()])
	# 	while not r.alinhaCor([r.sensorD.value()], 6, r.sensorD, r.sensorE, 0, 80):
	# 		continue


	# r.andarTempo(0, 300, 1000, True)
	# r.andarTempo(300, 0, 1000, True)
#Todo
# Comparaçao com HSV e sensor do meio em relação a sainda pista/aprendizagem/corAtual
# aperfeissuar teste de ruido e alinhaCor(Feito)"""