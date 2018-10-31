#!/usr/bin/env python3
from time import sleep
from classe import Robot

r = Robot('B', 'A', 'C', '1', '2', '3', '4', 6.5, 2.7, 13.5)
cores = ['unknown','black','blue','green','yellow','red','white','brown']

r.direcoes = []
r.cores = []
r.coresAprendidas = {5:90,4:-90,3:0}
while True:

	r.andarTempo(500, 500, 100)
	r.saindoPista()

	#Pega boneco
	if not r.garraOcupada:
		if r.detecta():
			r.modoAtaque()
	# if contBoneco = 50 and not bonecoGarra:
	# 	bonecoGarra = True
	# 	r.abreGarra(-1000, 300)

	#Pega Boneco Volta

	# Achou Cor
	if r.sensorE.value() not in [0, 1, 6, 7]:
		# print("Teste",r.teste)
		if not r.teste or r.obrigaTeste:
			while not r.alinhaCor([r.sensorE.value()], 6, r.sensorE, r.sensorD, 200, 0, True):
				continue
			r.andarTempo(400, 400, 700, True)

		if r.corAtual not in [int(key) for key in r.coresAprendidas.keys()]:
			r.aprendendoCor = True

			for direcao in r.direcoes:
				# print("Direcao", direcao)
				if direcao != 0: #Girar 0 de erro
					r.girar(direcao)
				r.saindoCor()
				r.obrigaTeste = False
				r.deadEnd(direcao)

				r.andarTempo(400, 400, 700, True)

				if r.aprendendoCor:
					ajusteGiro = direcao
					if direcao == 0:
						ajusteGiro = 180
					r.girar(ajusteGiro)
				else:
					print("Teste True")
					r.teste = True
					break
		else:
			# print("Cores Arepndida", r.coresAprendidas)
			# print(r.corAtual, r.voltaMapa)
			if r.corAtual == 3 and not r.voltaMapa:
				r.andarTempo(-200, -200, 750, True)
				if r.verificaEntradaPraca():
					#r.bateParede()
					# Luiz
					r.modoPraca(True)
					#############
					r.voltaPraca()
				else:
					direcao = r.coresAprendidas[r.corAtual]
					if direcao != 0:
						r.girar(direcao)
					r.aprendeMapa(r.corAtual)
					r.saindoCor()
			else:
				# print("Aprende Mapa")
				r.aprendeMapa(r.corAtual)
				if r.verificaMapa():
					r.reverteDirecao()
					r.girar(180)
					r.saindoCor()
				else:
					direcao = r.coresAprendidas[r.corAtual]
					if direcao != 0:
						r.girar(direcao)
					r.saindoCor()
	 		
		

	if r.sensorD.value() not in [0, 1, 6, 7]:
		# print("Teste",r.teste)
		if not r.teste or r.obrigaTeste:
			while not r.alinhaCor([r.sensorD.value()], 6, r.sensorD, r.sensorE, 0, 200, True):
				continue
			r.andarTempo(400, 400, 700, True)

		if r.corAtual not in [int(key) for key in r.coresAprendidas.keys()]:
			r.aprendendoCor = True
			for direcao in r.direcoes:
				# print("Direcao", direcao)
				if direcao != 0: #Girar 0 de erro
					r.girar(direcao)
				r.saindoCor()
				r.obrigaTeste = False
				r.deadEnd(direcao)

				r.andarTempo(400, 400, 700, True)
				# print("Aprendeu COr")
				if r.aprendendoCor:
					ajusteGiro = direcao
					if direcao == 0:
						ajusteGiro = 180
					r.girar(ajusteGiro)
				else:
					# print("Teste True")
					r.teste = True
					break
		else:
			# print("Cores Arepndida", r.coresAprendidas)
			# print(r.corAtual, r.voltaMapa)
			if r.corAtual == 3 and not r.voltaMapa:
				r.andarTempo(-200, -200, 750, True)
				if r.verificaEntradaPraca():
					r.bateParede()
					# r.girar(180)
					# Luiz
					r.modoPraca(r.garraOcupada)
					#############
					r.voltaPraca()
				else:
					direcao = r.coresAprendidas[r.corAtual]
					if direcao != 0:
						r.girar(direcao)
					r.aprendeMapa(r.corAtual)
					r.saindoCor()
			else:
				# print("Aprende Mapa")
				r.aprendeMapa(r.corAtual)
				if r.verificaMapa():
					r.reverteDirecao()
					r.girar(180)
					r.saindoCor()
				else:
					direcao = r.coresAprendidas[r.corAtual]
					if direcao != 0:
						r.girar(direcao)
					r.saindoCor()
	#Fim Achou Cor

# alinha cor(Feito)
# HSV->RGB && RGB->HSV (Feito)
# verifa com o sensor do meio (Feito)
# aprendendoCor  = True (Feito)
# testas as direções (Feito)
# teste de deadend (Feito)
# Vola deadEnd n tem teste de deadEnd(Feito)
# Ruido infinito(Feito)
# alinhaCor Branco(Feito)
# entrar Praça (Feito)
# inverter direções (Feito)
# volta (Feito)
# A mesma cor seguida duas vezes(Feito)

# verificar bola preta / largar boneco(Luiz)
# sair Praça(Luiz)

# mapa pista (Feito)
# Guarda todos de um lado
# Priorizar pegar boneco na no primeiro q for visto
# Merge dos códigos)