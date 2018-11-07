#!/usr/bin/env python3
from time import sleep
from ClasseRobo import ClasseRobo




robo = ClasseRobo('A', 'B', 'C', '1', '2', '3', '4', 6, 2.7, 13)
cores = ['unknown','black','blue','green','yellow','red','white','brown']

#robo.direcoes = []
#robo.cores = []
#robo.cores_aprendidas = {5:90, 4:-90, 3:0}
#robo.garra_ocupada = True
#robo.volta_mapa = True
#robo.mapa_simples = [4,5,4,3,4,5,5]

while True:
	robo.andarTempo(500, 500, 100)
	robo.saindoPista()

	if not robo.garra_ocupada:
		if robo.detectaBoneco():
			robo.modoAtaque()
	
	if robo.sensor_esquerdo.value() not in [0, 1, 6, 7]:
		if not robo.teste or robo.obriga_teste:
			while not robo.alinhaCor([robo.verificaCorSensor(robo.sensor_esquerdo)], 6, robo.sensor_esquerdo, robo.sensor_direito, 200, 0, True):
				continue
			robo.andarTempo(400, 400, 700, True)

		if robo.cor_atual not in [int(key) for key in robo.cores_aprendidas.keys()]:
			robo.aprendendo_cor = True

			for direcao in robo.direcoes:
				if direcao != 0:
					robo.girarRobo(direcao)
				robo.saindoCor()
				robo.obrigaTeste = False
				robo.deadEnd(direcao)

				robo.andarTempo(400, 400, 700, True)

				if robo.aprendendoCor:
					ajuste_giro = direcao
					if direcao == 0:
						ajuste_giro = 180
					robo.girarRobo(ajuste_giro)
				else:
					r.teste = True
					break
		else:
			if robo.cor_atual == 5 and not robo.volta_mapa:
				robo.andarTempo(-400, -400, 800, True)
				if robo.verificaEntradaPraca():
					robo.bateParede()
					robo.modoPraca(robo.garra_ocupada)
					robo.voltaPraca()
				else:
					direcao = robo.cores_aprendidas[robo.cor_atual]
					if direcao != 0:
						robo.girarRobo(direcao)
					robo.aprendeMapa(robo.cor_atual)
					robo.saindoCor()
	 		
		
	if robo.sensor_direito.value() not in [0, 1, 6, 7]:
		if not robo.teste or robo.obrigaTeste:
			while not robo.alinhaCor([robo.sensor_direito.value()], 6, robo.sensor_direito, robo.sensor_esquerdo, 0, 200, True):
				continue
			robo.andarTempo(400, 400, 700, True)

		if robo.cor_atual not in [int(key) for key in robo.cores_aprendidas.keys()]:
			robo.aprendendo_cor = True
			for direcao in robo.direcoes:
				if direcao != 0:
					robo.girarRobo(direcao)
				robo.saindoCor()
				robo.obrigaTeste = False
				robo.deadEnd(direcao)

				robo.andarTempo(400, 400, 700, True)
				if robo.aprendendo_cor:
					ajuste_giro = direcao
					if direcao == 0:
						ajuste_giro = 180
					robo.girarRobo(ajuste_giro)
				else:
					robo.teste = True
					break
		else:
			if robo.cor_atual == 5 and not robo.volta_mapa:
				robo.andarTempo(-400, -400, 800, True)
				if robo.verificaEntradaPraca():
					robo.bateParede()
					robo.modoPraca(robo.garra_ocupada)
					robo.voltaPraca()
				else:
					direcao = robo.cores_aprendidas[robo.cor_atual]
					if direcao != 0:
						robo.girarRobo(direcao)
					robo.aprendeMapa(robo.cor_atual)
					robo.saindoCor()