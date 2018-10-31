#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *
import math
from time import sleep

class Robot():

	def __init__(self, motorD, motorE, garra, sensorD, sensorE, sensorM, sensorU, R, r, dRodas):
		# Motores
		self.motorD = LargeMotor('out' + motorD)
		self.motorE = LargeMotor('out' + motorE)
		self.motorG = MediumMotor('out' + garra)
		# Sensores de Cor
		self.sensorD = ColorSensor('in' + sensorD)
		self.sensorD.mode = 'COL-COLOR'
		self.sensorE = ColorSensor('in' + sensorE)
		self.sensorE.mode = 'COL-COLOR'
		self.sensorM = ColorSensor('in' + sensorM)
		self.sensorM.mode = 'RGB-RAW'
		self.sensorU = UltrasonicSensor('in' + sensorU)
		assert self.sensorU.connected
		self.sensorU.mode = 'US-DIST-CM'
		# Odometria
		self.razao = self.odometria(R, r)
		self.razaoRoda = self.odometria(dRodas, r)
		self.razaoAndar = 2*math.pi*r
		# Variaveis
		self.corAtual = None
		self.aprendendoCor = False
		self.direcoes = [-90, 0, 90]
		self.cores = [3, 5, 4]
		self.coresAprendidas = {}
		self.printCores = ['unknown','black','blue','green','yellow','red','white','brown']
		self.mapeamento = True
		self.mapa = []
		self.mapaSimples = []
		self.mapaVolta = []
		self.voltaDeadEnd = False
		self.voltaMapa = False
		self.teste = False
		self.obrigaTeste = False
		self.garraOcupada = False


	def odometria(self, R, r):
		C = 2*math.pi*R
		c = 2*math.pi*r
		print("R:", C/c)
		return C/c

	def girar(self, g):
		girar = self.razao*g
		print("Girar",girar)
		self.andarRotacao(girar, -girar, 400, True)
		sleep(0.1)

	def girarRoda(self, graus):
		girarRoda = self.razaoRoda*graus
		self.andarRotacao(0, girarRoda, 400, True, True)
		sleep(0.1)
		return girarRoda

	def abreGarra(self, rotation, speed):
		self.motorG.run_to_rel_pos(position_sp=rotation, speed_sp=speed, stop_action="coast")
		self.motorG.wait_while('running')
		self.stop()
		return True

	def fechaGarra(self, speed):
		self.motorG.run_forever(speed_sp=speed)
		self.motorG.stop(stop_action='coast')
		return True

	def andarTempo(self, speed, speed2, time, wait = False):
		self.motorD.run_timed(time_sp = time, speed_sp = speed)
		self.motorE.run_timed(time_sp = time, speed_sp = speed2)
		# print(self.motorD.speed, self.motorE.speed)
		if wait:
			sleep(time/1000)
		return True

	def andarRotacao(self, rotation, rotation2, speed, wait = False, praca = False):
		self.motorD.run_to_rel_pos(position_sp=rotation, speed_sp=speed)
		self.motorE.run_to_rel_pos(position_sp=rotation2, speed_sp=speed)
		if wait and not praca:
			self.motorD.wait_while('running')
			self.motorE.wait_while('running')
		if praca:
			sleep(2)
			self.motorD.stop()
			self.motorE.stop()

	def stop(self):
		self.motorD.stop()
		self.motorE.stop()
		return True

	def ruido(self, cores, sensor, qtdTeste):
		ruido = 0
		for i in range(0, qtdTeste):
			if 0 <= i < qtdTeste/4 or qtdTeste/2 < i < 3*qtdTeste/4:
				self.andarTempo(100, 100, 100)
				if sensor.value() in cores:
					ruido += 1
					continue
			else:
				self.andarTempo(-100, -100, 100)
				if sensor.value() in cores:
						ruido += 1

		if ruido > round(qtdTeste*0.7):
			return True
		else:
			self.andarTempo(100, 100, 100, True)
		return False

	def controleSaindoCor(self):
		if self.sensorE.value() in [6]:
			if self.ruido([6], self.sensorE, 40):
				self.andarTempo(200, 0, 1000, True)
				if self.sensorD.value() in [6]:
					self.andarTempo(-400, 0, 400, True)
					return False
				else:
					self.andarTempo(-400, 0, 400, True)
					self.andarTempo(-300, -300, 300, True)
					self.andarTempo(0, 300, 250, True)
					self.andarTempo(300, 300, 300, True)
					return True


		if self.sensorD.value() in [6]:
			if self.ruido([6], self.sensorD, 40):
				self.andarTempo(0, 200, 1000, True)
				if self.sensorE.value() in [6]:
					self.andarTempo(0, -400, 400, True)
					return False
				else:
					self.andarTempo(0, -400, 400, True)
					self.andarTempo(-300, -300, 300, True)
					self.andarTempo(0, 300, 250, True)
					self.andarTempo(300, 300, 300, True)
					return True

	def saindoPista(self):
		if self.aprendendoCor:
			if self.sensorE.value() in [1] and not self.voltaDeadEnd:
				if self.ruido([1], self.sensorE, 70):
					self.andarTempo(200, 0, 1000, True)
					if self.sensorD.value() in [1]:
						self.andarTempo(-200, 0, 1000, True)
						self.girar(180)
						self.voltaDeadEnd = True
						return True
					else:
						self.andarTempo(-200, 0, 1000, True)

			if self.sensorD.value() in [1] and not self.voltaDeadEnd:
				if self.ruido([1], self.sensorD, 70):
					self.andarTempo(0, 200, 1000, True)
					if self.sensorE.value() in [1]:
						self.andarTempo(0, -200, 1000, True)
						self.girar(180)
						self.voltaDeadEnd = True
						return True
					else:
						self.andarTempo(0, -200, 1000, True)
		# Na volta de um dead end n fazer teste de deadEnd

		if self.sensorE.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensorE, 20):
				self.andarTempo(-300, -300, 300, True)
				self.andarTempo(0, 300, 250, True)
				self.andarTempo(300, 300, 300, True)
				return True

		if self.sensorD.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensorD, 20):
				self.andarTempo(-300, -300, 300, True)
				self.andarTempo(300, 0, 250, True)
				self.andarTempo(300, 300, 300, True)
				return True

		return False

	def alinhaCor(self, cor, corAlinhamento,sensorEntrada, sensorAjuste, velocidadeMotorEntrada, velocidadeMotorAjuste, updateCor = False, garra = False):
		print("Alinha", cor, corAlinhamento)
		if self.ruido(cor, sensorEntrada, 5):
			if self.ruido(cor, sensorEntrada, 40):
				while sensorEntrada.value() != corAlinhamento:
					self.andarTempo(-velocidadeMotorAjuste, -velocidadeMotorEntrada, 100)
					# if not garra:
					# 	if self.saindoPista():
					# 		return True
				while sensorAjuste.value() not in cor:
					self.andarTempo(velocidadeMotorEntrada, velocidadeMotorAjuste, 100)
					# if not garra:
					# 	if self.saindoPista():
					# 		return True
				while sensorAjuste.value() != corAlinhamento:
					self.andarTempo(-velocidadeMotorEntrada, -velocidadeMotorAjuste, 100)
					# if not garra:
					# 	if self.saindoPista():
					# 		return True

				if not garra:
					while self.verificaCor() not in cor:
						self.andarTempo(500, 500, 100)

				if updateCor:
					self.verificaCor(True)
				return True 
			else: 
				return False
		else:
			return False

	def verificaCor(self, setCor = False):
		r = self.sensorM.value(0)
		g = self.sensorM.value(1)
		b = self.sensorM.value(2)

		hsv = self.convertHSV([r, g, b])
		hsv[2] = 100
		rgb = self.convertRGB(hsv)

		if setCor:
			self.corAtual = self.readColor(rgb)
		return self.readColor(rgb)

	def saindoCor(self):
		while True:	
			self.andarTempo(500, 500, 100)
			self.saindoPista()
			print(self.sensorE.value(), self.sensorD.value())
			if self.sensorE.value() == 6 and self.sensorE.value() != self.corAtual:
				#if self.controleSaindoCor():
					#continue
				if self.ruido([6], self.sensorE, 60):
					while not self.alinhaCor([6], self.corAtual, self.sensorE, self.sensorD, 300, 0):
						continue
				self.teste = False
				return True

			if self.sensorD.value() == 6 and self.sensorD.value() != self.corAtual:
				#if self.controleSaindoCor():
					#continue
				if self.ruido([6], self.sensorD, 60):
					while not self.alinhaCor([6], self.corAtual, self.sensorD, self.sensorE, 0, 300):
						continue
				self.teste = False
				return True

	def codigoPraca(self, cor):
		while True:	
			self.andarTempo(500, 500, 100)
			self.saindoPista()

			if self.sensorE.value() == 6 and self.sensorE.value() != self.corAtual:
				if self.ruido([6], self.sensorE, 100):
					while not self.alinhaCor([6], self.corAtual, self.sensorE, self.sensorD, 300, 0):
						continue
					self .andarTempo(-300, -300, 1100, True)
				return False

			if self.sensorD.value() == 6 and self.sensorD.value() != self.corAtual:
				if self.ruido([6], self.sensorD, 100):
					while not self.alinhaCor([6], self.corAtual, self.sensorD, self.sensorE, 0, 300):
						continue
				self.andarTempo(-300, -300, 1100, True)
				return False

			if self.sensorE.value() == cor and self.sensorE.value() != self.corAtual:
				if self.ruido([cor], self.sensorE, 100):
					while not self.alinhaCor([cor], self.corAtual, self.sensorE, self.sensorD, 200, 0):
						continue
				return True

			if self.sensorD.value() == cor and self.sensorD.value() != self.corAtual:
				if self.ruido([cor], self.sensorD, 100):
					while not self.alinhaCor([cor], self.corAtual, self.sensorD, self.sensorE, 0, 200):
						continue
				return True

	def voltandoCor(self, direcao):
		if self.sensorE.value() in [self.corAtual] and self.voltaDeadEnd:
			while not self.alinhaCor([self.sensorE.value()], 6, self.sensorE, self.sensorD, 300, 0):
				continue
			while self.verificaCor() != self.corAtual:
				self.andarTempo(500, 500, 100)
			return False

		if self.sensorD.value() in [self.corAtual] and self.voltaDeadEnd:
			while not self.alinhaCor([self.sensorD.value()], 6, self.sensorD, self.sensorE, 0, 300):
				continue
			while self.verificaCor() != self.corAtual:
				self.andarTempo(500, 500, 100)
			return False
		return True

	def novaCor(self, direcao):
		if self.sensorE.value() not in [0, 1, 6, 7, self.corAtual]:
			if self.ruido([self.sensorE.value()], self.sensorE, 70):
				tempCor = self.sensorE.value()
				while not self.alinhaCor([self.sensorE.value()], 6, self.sensorE, self.sensorD, 300, 0):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(500, 500, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.corAtual, direcao)
				self.verificaCor(True)
				self.aprendendoCor = False
				return False

		if self.sensorD.value() not in [0, 1, 6, 7, self.corAtual]:
			if self.ruido([self.sensorD.value()], self.sensorD, 70):
				tempCor = self.sensorD.value()
				while not self.alinhaCor([self.sensorD.value()], 6, self.sensorD, self.sensorE, 0, 300):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(400, 400, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.corAtual, direcao)
				self.verificaCor(True)
				self.aprendendoCor = False
				return False

		if self.sensorE.value() in [self.corAtual] and not self.voltaDeadEnd:
			if self.ruido([self.sensorE.value()], self.sensorE, 70):
				tempCor = self.sensorE.value()
				while not self.alinhaCor([self.sensorE.value()], 6, self.sensorE, self.sensorD, 300, 0,  True):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(500, 500, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.corAtual, direcao)
				self.verificaCor(True)
				self.aprendendoCor = False
				self.andarTempo(400, 400, 600, True)
				self.aprendeMapa(self.corAtual)
				direcao = self.coresAprendidas[self.corAtual]
				if direcao != 0:
					self.girar(direcao)
				self.saindoCor()
				self.obrigaTeste = True
				return False

		if self.sensorD.value() in [self.corAtual] and not self.voltaDeadEnd:
			if self.ruido([self.sensorD.value()], self.sensorD, 70):
				tempCor = self.sensorD.value()
				while not self.alinhaCor([self.sensorD.value()], 6, self.sensorD, self.sensorE, 0, 300, True):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(400, 400, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.corAtual, direcao)
				self.verificaCor(True)
				self.aprendendoCor = False
				self.andarTempo(400, 400, 600, True)
				self.aprendeMapa(self.corAtual)
				direcao = self.coresAprendidas[self.corAtual]
				if direcao != 0:
					self.girar(direcao)
				self.saindoCor()
				self.obrigaTeste = True
				return False
		return True



	def deadEnd(self, direcao):
		while True:
			# print("DeadEnd")
			self.andarTempo(500, 500, 100)
			self.saindoPista()
			if not self.garraOcupada and not self.voltaDeadEnd:
				if self.detecta():
					self.modoAtaque()

			# voltar para  a mesma cor
			if not self.voltandoCor(direcao):
				self.voltaDeadEnd = False
				return False

			# nova cor
			if not self.novaCor(direcao):
				self.voltaDeadEnd = False
				return False
			
		return True

	def aprende(self, cor, direcao):
		if len(self.direcoes) == 3:
			self.coresAprendidas.update({cor: direcao})
			self.cores.remove(cor)
			self.direcoes.remove(direcao)
			if self.mapeamento:
				self.aprendeMapa(cor)

		elif len(self.direcoes) == 2:
			self.coresAprendidas.update({cor: direcao})
			self.cores.remove(cor)
			self.direcoes.remove(direcao)
			if self.mapeamento:
				self.aprendeMapa(cor)

			self.coresAprendidas.update({self.cores[0]: self.direcoes[0]})
			self.cores.remove(self.cores[0])
			self.direcoes.remove(self.direcoes[0])
		else:
			print("Erro com aprende()")

	def convertHSV(self, rgb):
		r = rgb[0]/255
		g = rgb[1]/255
		b = rgb[2]/255
		_min = min(r, g, b)
		_max = max(r, g, b)
		delta = _max - _min

		# set H
		if delta == 0:
			h = 0
		elif _max == r:
			h = float(60*(((g-b)/delta)%6))
		elif _max == g:
			h = float(60*(((b-r)/delta)+2))
		elif _max == b:
			h = float(60*(((r-g)/delta)+4))

		# ser S
		if delta == 0:
			s = 0
		else:
			s = float(100*delta/_max)

		# set V
		v = 100*_max

		h = round(h, 2)
		s = round(s, 2)
		v = round(v, 2)

		return [h, s, v]

	def convertRGB(self, hsv):
		h = float(hsv[0])
		s = float(hsv[1]/100)
		v = float(hsv[2]/100)

		c = float(v*s)
		x = float(c*(1 - abs(((h/60)%2)-1)))
		m = float(v-c)

		if 0 <= h < 60:
			r = c
			g = x
			b = 0
		elif 60 <= h < 120:
			r = x
			g = c
			b = 0
		elif 120 <= h < 180:
			r = 0
			g = c
			b = x
		elif 180 <= h < 240:
			r = 0
			g = x
			b = c
		elif 240 <= h < 300:
			r = x
			g = 0
			b = c
		elif 300 <= h < 360:
			r = c
			g = 0
			b = x

		r = round((r+m))
		g = round((g+m))
		b = round((b+m))

		return [r,g,b]

	def readColor(self, rgb):
		r = rgb[0]
		g = rgb[1]
		b = rgb[2]

		if r == 1:
			if g ==  1:
				if b == 1:
					return 6
				else:
					return 4
			else:
				if b == 1:
					return 5
				else:
					return 5
		else:
			if g == 1:
				if b == 1:
					return 2
				else:
					return 3
			else:
				if b == 1:
					return 2
				else:
					return 1

	def verificaEntradaPraca(self):
		if self.codigoPraca(5):
			self.verificaCor(True)
			if self.codigoPraca(4):
				self.verificaCor(True)
				self.saindoCor()
				return True
		return False

	def aprendeMapa(self, cor, atualiza = False):
		if self.mapeamento:
			self.mapa.append({cor: True})
			self.mapaSimples.append(cor)

		if self.voltaMapa:
			self.mapaVolta.append(cor)	

		print("Aprendendo Mapa", self.mapaSimples, self.mapaVolta, list(reversed(self.mapaVolta)))		

		if atualiza:
			print('atualiza mapa')

	def verificaMapa(self):
		print(self.mapaSimples, self.mapaVolta, list(reversed(self.mapaVolta)))
		if list(reversed(self.mapaVolta)) == self.mapaSimples:
			self.voltaMapa = False
			self.mapaVolta = []
			return True
		return False
		
	def reverteDirecao(self):
		for i in [int(key) for key in self.coresAprendidas.keys()]:
			self.coresAprendidas[i] *= -1

	def voltaPraca(self):
		self.mapeamento = False
		self.voltaMapa = True
		self.reverteDirecao()

		while True:
			self.andarTempo(500,500,100)
			self.saindoPista()

			if self.sensorD.value() in [4]:
				while not self.alinhaCor([4], 6, self.sensorD, self.sensorE, 0, 300, True):
					continue
				break

			if self.sensorE.value() in [4]:
				while not self.alinhaCor([4], 6, self.sensorE, self.sensorD, 300, 0, True):
					continue
				break

		if self.codigoPraca(5):
			self.verificaCor(True)
			if self.codigoPraca(3):
				self.verificaCor(True)
				self.saindoCor()
				return True
		return True

	# Garra Luiz
	def detecta(self):
		print("Detecta:", self.sensorU.value())
		if(self.sensorU.value() < 250):
			return True
		return False

	def detectaParede(self):
		if(self.sensorU.value() < 300):
			return True
		return False

	def abreGarra(self, rotation, speed, wait = False):
		self.motorG.run_to_rel_pos(position_sp=rotation, speed_sp=speed)
		if wait:
			self.motorG.wait_while('running',2000)
		return True

	def pegaBoneco(self, garraOcupada):
		# print('entrou pega boneco')
		if not garraOcupada:
			self.motorG.stop()
			self.abreGarra(-1440,600,True)
			garraOcupada = True
		return garraOcupada

	def largaBoneco(self, garraOcupada):
		if garraOcupada:
			self.motorG.stop()
			self.abreGarra(1440,600, True)
			garraOcupada = False
			print('largaboneco',garraOcupada)
		return garraOcupada

	def medeHipotenusaBoneco(self):
		hipotenusaBoneco = 0	
		for x in range(3):
			if self.detecta():
				hipotenusaBoneco = (self.sensorU.value()/10)
				self.andarRotacao(-35,-35,50, True)
				print(hipotenusaBoneco)
			if not self.detecta():
				self.andarRotacao(35,35,50, True)
				print(hipotenusaBoneco)
		self.stop = True
		return True
	def medeHipotenusaParede(self):	
		hipotenusaParede = 0	
		if self.detectaParede():
			hipotenusaParede = (self.sensorU.value()/10)
			self.andarRotacao(-70,-70,50, True)
			print(hipotenusaParede)
		if not self.detectaParede():
			self.andarRotacao(70,70,50, True)
			print(hipotenusaParede)
		return hipotenusaParede

	def modoAtaque(self):
		#self.detectou = self.detecta()
		contDetecta = 0
		while not self.garraOcupada: #and self.detectou == True: #se a garra estiver ocupada ele não tenta detectar
			#CODIGO DO LUIS
			# while not self.detecta(): #enquanto ele não detecta ele anda
			# 	self.andarTempo(300,300,600)
			# if self.detecta(): #se ele detecta ele faz teste de ruído e gira
			# 	self.medeHipotenusaBoneco()
			# 	self.girar(-90)
			# 	print('girou')

			#CODIGO LUCAS
			self.andarTempo(-300,-300,200,True)
			for i in range(5):
				if not self.detecta():
					self.andarTempo(300,300,100, True)
				print(i)
				sleep(0.5)
			print("What:", self.detecta())
			if self.detecta(): #se ele detecta ele faz teste de ruído e gira
				self.medeHipotenusaBoneco()
				self.girar(-90)
				print('girou')
			else:
				self.andarTempo(-300,-300, 400, True)
				return False

			if self.voltaMapa:
				self.girar(180)
				self.voltaMapa = False
				self.mapaVolta = []
				self.reverteDirecao()
				return True

		
			while self.sensorE.value() not in [0,1,7] and self.sensorD.value() not in [0,1,7]: #enquanto o valor dos sensores não chegar em preto ou marrom/unknown ele anda
				self.andarTempo(100,100,100)
				print(self.sensorE.value(),self.sensorD.value())
			if self.sensorE.value() in [0,1,7]: #se o sensor tiver em preto ou marrom/unknown ele tenta alinhar
				while not self.alinhaCor([0,1,7], 6, self.sensorE, self.sensorD, 100, 0, False, True):
					continue
			if self.sensorD.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensorD, self.sensorE, 0, 100, False, True):
					continue
			self.girarRoda(-90)
			self.andarTempo(-200,-200,500, True)
			print('girou de novo')
			while not self.detecta():
				self.andarTempo(300,300,600)
			if self.detecta():
				self.medeHipotenusaBoneco()
				self.andarTempo(-300,-300,500,True)
				self.girar(-90)
			self.andarTempo(-600,-600,500, True)
			self.garraOcupada = self.pegaBoneco(self.garraOcupada)
			print(self.garraOcupada)
			print('modo ataque',self.garraOcupada)
			self.andarTempo(600,600,500, True)
			self.girar(90)
			#return garraOcupada
			############################
			############SÓ TESTE########

	# Praca Luiz
	def bateParede(self):
		i = 0
		d = 0
		e = 0
		seguidos = 0
		bol = True
		for i in range(100):
			self.andarTempo(400, 400, 100)
			if (self.motorE.speed < 350) and i > 10:
				e += 1
				bol = False
			if (self.motorD.speed < 350) and i > 10:
				d += 1
				bol = False

			if bol:
				e = 0
				d = 0

			if e > 3:
				self.andarTempo(-200,-200, 600, True)
				self.andarTempo(-300, 0, 400, True)
				self.andarTempo(200, 200, 600, True)
				e = 0
				d = 0
			if d > 3:
				self.andarTempo(-200,-200, 600, True)
				self.andarTempo(0, -300, 400, True)
				self.andarTempo(200, 200, 600, True)
				e = 0
				d = 0

			bol = True

		return True

	def modoPraca(self, garraOcupada):
		c = 0
		i = 0
		dist1 = 0
		dist2 = 0
		distm = 0
		hipotenusa = 0
		angulo = 0
		distpercorrida = 0
		if self.garraOcupada:
			while self.sensorE.value() not in [0,1,7] or self.sensorD.value() not in [0,1,7]:
				self.andarTempo(200,200,100)
				c = c+1
			if self.sensorE.value() in [0,1,7]: #se o sensor tiver em preto ou marrom/unknown ele tenta alinhar
				while not self.alinhaCor([0,1,7], 6, self.sensorE, self.sensorD, 100, 0, False, True):
					continue
			if self.sensorD.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensorD, self.sensorE, 0, 100, False, True):
					continue
			self.girar(180)			
			self.voltar = True
			print(c,i)
			self.garraOcupada = self.largaBoneco(self.garraOcupada)
		while i < c-150:
			self.andarTempo(125,125,100)
			i = i + 1
			print(c,i)
		self.girar(-90)
		while not self.detectaParede():
			self.andarTempo(-100,-100,100)
		if self.detectaParede():
			self.andarTempo(-125,-125,400,True)
			self.medeHipotenusaParede()
			dist1 = self.medeHipotenusaParede()
			self.andarRotacao(-360,-360,400,True)
			dist2 = self.medeHipotenusaParede()
			if (dist1 < dist2) :
				distm = (dist2 - dist1)
				print("primeiro if",dist1,dist2)
				hipotenusa = self.razaoAndar
				angulo = math.acos(distm/hipotenusa)*(180/math.pi)
				angulo = 90 - angulo
				print(distm)
				print('angulo eh',angulo)
				girarRoda = self.girarRoda(angulo)
				print('debug1')
			else:
				distm = (dist1-dist2)
				print("segundo if",dist1,dist2)
				hipotenusa = self.razaoAndar
				angulo = math.acos(distm/hipotenusa)*(180/math.pi)
				angulo = 90 - angulo
				print(distm)
				print('angulo 2 eh',angulo)
				girarRoda = self.girarRoda(-angulo)
				print("debug",girarRoda)
				self.andarTempo(100,100,100,True)
		while self.detectaParede():
			print("entrou while")
			self.andarTempo(100,100,100)
		if not self.detectaParede():
			print("entrou no buraco")
			self.andarTempo(75,75,100)
			self.girar(90)
		while i<c-10:
			self.andarTempo(100,100,100)
			i = i + 1

		return True

# mB.stop()
# mC.stop()