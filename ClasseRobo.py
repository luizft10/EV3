#!/usr/bin/env python3
from ev3dev.ev3 import *
import math
from time import sleep





class ClasseRobo():

	def __init__(self, motor_direito, motor_esquerdo, motor_garra, sensor_direito, sensor_esquerdo, sensor_meio, sensor_ultrasonico, distancia_centro, raio_roda, distancia_rodas):
		self.motor_direito = LargeMotor('out' + motor_direito)
		self.motor_esquerdo = LargeMotor('out' + motor_esquerdo)

		self.sensor_direito = ColorSensor('in' + sensor_direito)
		self.sensor_esquerdo = ColorSensor('in' + sensor_esquerdo)
		self.sensor_meio = ColorSensor('in' + sensor_meio)
		self.sensor_ultrasonico = UltrasonicSensor('in' + sensor_ultrasonico)
		assert self.sensor_ultrasonico.connected

		self.sensor_direito.mode = 'COL-COLOR'
		self.sensor_esquerdo.mode = 'COL-COLOR'
		self.sensor_meio.mode = 'RGB-RAW'
		self.sensor_ultrasonico.mode = 'US-DIST-CM'

		self.razao_robo = self.odometria(distancia_centro, raio_roda)
		self.razao_roda = self.odometria(distancia_rodas, raio_roda)
		self.razao_andar = 2 * math.pi * raio_roda

		self.garra_ocupada = False

		self.cor_atual = None
		self.aprendendo_cor = False
		self.direcoes = [-90, 0, 90]
		self.cores = [3, 5, 2]
		self.cores_aprendidas = {}
		self.mapeamento = True
		self.mapa = []
		self.mapa_simples = []
		self.mapa_volta = []
		self.volta_dead_end = False
		self.volta_mapa = False
		self.teste = False
		self.obriga_teste = False

		

	def odometria(self, R, r):
		C = 2 * math.pi * R
		c = 2 * math.pi * r
		return C/c



	def girarRobo(self, g):
		girar = self.razao_robo * g
		self.andarRotacao(girar, -girar, 400, True)
		sleep(0.1)



	def girarRoda(self, graus):
		girarRoda = self.razao_roda * graus
		print(girarRoda)
		self.andarRotacao(0, girarRoda, 400, True)
		sleep(0.005)
		return girarRoda



	def andarRoda(self, roda, graus):
		angulo = self.razao_roda * graus
		if roda == "d":
			self.andarRotacao(0, angulo, 400, True, True)

		if roda == "e":
			self.andarRotacao(angulo, 0, 400, True, True)



	def andarTempo(self, speed, speed2, time, wait = False):
		self.motor_direito.run_timed(time_sp = time, speed_sp = speed)
		self.motor_esquerdo.run_timed(time_sp = time, speed_sp = speed2)
		if wait:
			sleep(time/1000)
		return True



	def andarRotacao(self, rotation, rotation2, speed, wait = False, praca = False):
		self.motor_direito.run_to_rel_pos(position_sp = rotation, speed_sp = speed)
		self.motor_esquerdo.run_to_rel_pos(position_sp = rotation2, speed_sp = speed)
		if wait and not praca:
			self.motor_direito.wait_while('running')
			self.motor_esquerdo.wait_while('running')
		if praca:
			sleep(1)
			self.motor_direito.stop()
			self.motor_esquerdo.stop()



	def parar(self):
		self.motor_direito.stop()
		self.motor_esquerdo.stop()
		return True



	def detectaBoneco(self):
		if (self.sensor_ultrasonico.value() < 250):
			return True
		return False



	def detectaParede(self):
		if (self.sensor_ultrasonico.value() < 300):
			return True
		return False



	def ruido(self, cores, sensor, quantidade_testes):
		ruido = 0
		for i in range(0, quantidade_testes):
			if 0 <= i < quantidade_testes/4 or quantidade_testes/2 < i < 3 * quantidade_testes/4:
				self.andarTempo(100, 100, 100)
				if sensor.value() in cores:
					ruido += 1
					continue
			else:
				self.andarTempo(-100, -100, 100)
				if sensor.value() in cores:
						ruido += 1

		if ruido > round(quantidade_testes * 0.7):
			return True
		else:
			self.andarTempo(100, 100, 100, True)
		return False



	def controleSaindoCor(self):
		if self.sensor_esquerdo.value() in [6]:
			if self.ruido([6], self.sensor_esquerdo, 40):
				self.andarTempo(400, 0, 300, True)
				if self.sensor_direito.value() in [6]:
					self.andarTempo(-400, 0, 300, True)
					return False
				else:
					self.andarTempo(-400, 0, 300, True)
					self.andarTempo(-300, -300, 300, True)
					self.andarTempo(0, 300, 250, True)
					self.andarTempo(300, 300, 300, True)
					return True


		if self.sensor_direito.value() in [6]:
			if self.ruido([6], self.sensor_direito, 40):
				self.andarTempo(0, 400, 300, True)
				if self.sensor_esquerdo.value() in [6]:
					self.andarTempo(0, -400, 300, True)
					return False
				else:
					self.andarTempo(0, -400, 300, True)
					self.andarTempo(-300, -300, 300, True)
					self.andarTempo(0, 300, 250, True)
					self.andarTempo(300, 300, 300, True)
					return True



	def saindoPista(self):
		if self.aprendendo_cor:
			if self.sensor_esquerdo.value() in [1] and not self.volta_dead_end:
				if self.ruido([1], self.sensor_esquerdo, 70):
					self.andarTempo(400, 0, 500, True)
					if self.sensor_direito.value() in [1]:
						self.andarTempo(-400, 0, 500, True)
						self.girarRobo(180)
						self.voltaDeadEnd = True
						return True
					else:
						self.andarTempo(-400, 0, 500, True)

			if self.sensor_direito.value() in [1] and not self.volta_dead_end:
				if self.ruido([1], self.sensor_direito, 70):
					self.andarTempo(0, 400, 500, True)
					if self.sensor_esquerdo.value() in [1]:
						self.andarTempo(0, -400, 500, True)
						self.girarRobo(180)
						self.volta_dead_end = True
						return True
					else:
						self.andarTempo(0, -400, 500, True)

		if self.sensor_esquerdo.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensor_esquerdo, 20):
				self.andarTempo(-300, -300, 300, True)
				self.andarTempo(0, 300, 250, True)
				self.andarTempo(300, 300, 300, True)
				return True

		if self.sensor_direito.value() in [0,1,7]:
			if self.ruido([0,1,7], self.sensor_direito, 20):
				self.andarTempo(-300, -300, 300, True)
				self.andarTempo(300, 0, 250, True)
				self.andarTempo(300, 300, 300, True)
				return True

		return False



	def alinhaCor(self, cor, cor_alinhamento, sensor_entrada, sensor_ajuste, velocidade_motor_entrada, velocidade_motor_ajuste, atualiza_cor = False, garra = False):
		if self.ruido(cor, sensor_entrada, 5):
			if self.ruido(cor, sensor_entrada, 40):
				while sensor_entrada.value() != cor_alinhamento:
					self.andarTempo(-velocidade_motor_ajuste, -velocidade_motor_entrada, 100)

				while sensor_ajuste.value() not in cor:
					if self.cor_atual == 2:
						self.andarTempo(velocidade_motor_entrada, velocidade_motor_ajuste, 100)
						break
					self.andarTempo(-velocidade_motor_entrada, velocidade_motor_ajuste, 100)

				while sensor_ajuste.value() != cor_alinhamento:
					self.andarTempo(-velocidade_motor_entrada, -velocidade_motor_ajuste, 100)

				if not garra:
					while self.verifica_cor() not in cor:
						self.andarTempo(500, 500, 100)

				if atualiza_cor:
					self.verificaCor(True)
				return True 
			else: 
				return False
		else:
			return False



	def verificaCor(self, muda_cor = False):
		r = self.sensor_meio.value(0)
		g = self.sensor_meio.value(1)
		b = self.sensor_meio.value(2)

		hsv = self.converteHSV([r, g, b])
		hsv[2] = 100
		rgb = self.converteRGB(hsv)

		if muda_cor:
			self.cor_atual = self.leCor(rgb)
		return self.leCor(rgb)


	
	def verificaCorSensor(self, sensor, muda_cor = False):
		sensor.mode = 'RGB_RAW'

		r = sensor.value(0)
		g = sensor.value(1)
		b = sensor.value(2)

		hsv = self.converteHSV([r, g, b])
		hsv[2] = 100
		rgb = self.converteRGB(hsv)

		if muda_cor:
			self.cor_atual = self.leCor(rgb)

		sensor.mode = 'COL-COLOR'

		return self.leCor(rgb)



	def saindoCor(self):
		while True:	
			self.andarTempo(500, 500, 100)
			self.saindoPista()
			if self.sensor_esquerdo.value() == 6 and self.sensor_esquerdo.value() != self.cor_atual:
				if self.controleSaindoCor():
					continue
				if self.ruido([6], self.sensor_esquerdo, 60):
					while not self.alinhaCor([6], self.cor_atual, self.sensor_esquerdo, self.sensor_direito, 300, 0):
						continue
				self.teste = False
				return True

			if self.sensor_direito.value() == 6 and self.sensor_direito.value() != self.cor_atual:
				if self.controleSaindoCor():
					continue
				if self.ruido([6], self.sensor_direito, 60):
					while not self.alinhaCor([6], self.cor_atual, self.sensor_direito, self.sensor_esquerdo, 0, 300):
						continue
				self.teste = False
				return True



	def codigoPraca(self, cor):
		while True:	
			self.andarTempo(700, 700, 100)
			self.saindoPista()

			if self.sensor_esquerdo.value() == 6 and self.sensor_esquerdo.value() != self.cor_atual:
				if self.ruido([6], self.sensor_esquerdo, 100):
					while not self.alinhaCor([6], self.cor_atual, self.sensor_esquerdo, self.sensor_direito, 300, 0):
						continue
					self.andarTempo(-300, -300, 1100, True)
				return False

			if self.sensor_direito.value() == 6 and self.sensor_direito.value() != self.cor_atual:
				if self.ruido([6], self.sensor_direito, 100):
					while not self.alinhaCor([6], self.cor_atual, self.sensor_direito, self.sensor_esquerdo, 0, 300):
						continue
				self.andarTempo(-300, -300, 1100, True)
				return False

			if self.sensor_esquerdo.value() == cor and self.sensor_esquerdo.value() != self.cor_atual:
				if self.ruido([cor], self.sensor_esquerdo, 100):
					while not self.alinhaCor([cor], self.cor_atual, self.sensor_esquerdo, self.sensor_direito, 200, 0):
						continue
				return True

			if self.sensor_direito.value() == cor and self.sensor_direito.value() != self.cor_atual:
				if self.ruido([cor], self.sensor_direito, 100):
					while not self.alinhaCor([cor], self.cor_atual, self.sensor_direito, self.sensor_esquerdo, 0, 200):
						continue
				return True



	def voltandoCor(self, direcao):
		if self.sensor_esquerdo.value() in [self.cor_atual] and self.voltaDeadEnd:
			while not self.alinhaCor([self.sensor_esquerdo.value()], 6, self.sensor_esquerdo, self.sensor_direito, 300, 0):
				continue
			while self.verificaCor() != self.cor_atual:
				self.andarTempo(500, 500, 100)
			return False

		if self.sensor_direito.value() in [self.cor_atual] and self.voltaDeadEnd:
			while not self.alinhaCor([self.sensor_direito.value()], 6, self.sensor_direito, self.sensor_esquerdo, 0, 300):
				continue
			while self.verificaCor() != self.cor_atual:
				self.andarTempo(500, 500, 100)
			return False
		return True



	def novaCor(self, direcao):
		if self.sensor_esquerdo.value() not in [0, 1, 6, 7, self.cor_atual]:
			if self.ruido([self.sensor_esquerdo.value()], self.sensor_esquerdo, 70):
				tempCor = self.sensor_esquerdo.value()
				while not self.alinhaCor([self.sensor_esquerdo.value()], 6, self.sensor_esquerdo, self.sensor_direito, 300, 0):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(500, 500, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.cor_atual, direcao)
				self.verificaCor(True)
				self.aprendendo_cor = False
				return False

		if self.sensor_direito.value() not in [0, 1, 6, 7, self.cor_atual]:
			if self.ruido([self.sensor_direito.value()], self.sensor_direito, 70):
				tempCor = self.sensor_direito.value()
				while not self.alinhaCor([self.sensor_direito.value()], 6, self.sensor_direito, self.sensor_esquerdo, 0, 300):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(400, 400, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.cor_atual, direcao)
				self.verificaCor(True)
				self.aprendendo_cor = False
				return False

		if self.sensor_esquerdo.value() in [self.cor_atual] and not self.voltaDeadEnd:
			if self.ruido([self.sensor_esquerdo.value()], self.sensor_esquerdo, 70):
				tempCor = self.sensor_esquerdo.value()
				while not self.alinhaCor([self.sensor_esquerdo.value()], 6, self.sensor_esquerdo, self.sensor_direito, 300, 0,  True):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(500, 500, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.cor_atual, direcao)
				self.verificaCor(True)
				self.aprendendo_cor = False
				self.andarTempo(400, 400, 600, True)
				self.aprendeMapa(self.cor_atual)
				direcao = self.cores_aprendidas[self.cor_atual]
				if direcao != 0:
					self.girarRobo(direcao)
				self.saindoCor()
				self.obriga_teste = True
				return False

		if self.sensor_direito.value() in [self.cor_atual] and not self.voltaDeadEnd:
			if self.ruido([self.sensor_direito.value()], self.sensor_direito, 70):
				tempCor = self.sensor_direito.value()
				while not self.alinhaCor([self.sensor_direito.value()], 6, self.sensor_direito, self.sensor_esquerdo, 0, 300, True):
					continue

				while self.verificaCor() != tempCor:
					self.andarTempo(400, 400, 100)
				self.andarTempo(300, 300, 200, True)
				self.aprende(self.cor_atual, direcao)
				self.verificaCor(True)
				self.aprendendo_cor = False
				self.andarTempo(400, 400, 600, True)
				self.aprendeMapa(self.cor_atual)
				direcao = self.cores_aprendidas[self.cor_atual]
				if direcao != 0:
					self.girarRobo(direcao)
				self.saindoCor()
				self.obriga_teste = True
				return False
		return True



	def deadEnd(self, direcao):
		while True:
			self.andarTempo(500, 500, 100)
			self.saindoPista()
			if not self.garra_ocupada and not self.voltaDeadEnd:
				if self.detectaBoneco():
					self.modoAtaque()

			if not self.voltandoCor(direcao):
				self.voltaDeadEnd = False
				return False

			if not self.novaCor(direcao):
				self.voltaDeadEnd = False
				return False
			
		return True



	def aprende(self, cor, direcao):
		if len(self.direcoes) == 3:
			self.cores_aprendidas.update({cor: direcao})
			self.cores.remove(cor)
			self.direcoes.remove(direcao)
			if self.mapeamento:
				self.aprendeMapa(cor)

		elif len(self.direcoes) == 2:
			self.cores_aprendidas.update({cor: direcao})
			self.cores.remove(cor)
			self.direcoes.remove(direcao)
			if self.mapeamento:
				self.aprendeMapa(cor)

			self.cores_aprendidas.update({self.cores[0]: self.direcoes[0]})
			self.cores.remove(self.cores[0])
			self.direcoes.remove(self.direcoes[0])



	def converteHSV(self, rgb):
		r = rgb[0]/255
		g = rgb[1]/255
		b = rgb[2]/255
		_min = min(r, g, b)
		_max = max(r, g, b)
		delta = _max - _min

		if delta == 0:
			h = 0
		elif _max == r:
			h = float(60 * (((g - b)/delta) % 6))
		elif _max == g:
			h = float(60 * (((b - r)/delta) + 2))
		elif _max == b:
			h = float(60 * (((r - g)/delta) + 4))

		if delta == 0:
			s = 0
		else:
			s = float(100 * delta/_max)

		v = 100 * _max

		h = round(h, 2)
		s = round(s, 2)
		v = round(v, 2)

		return [h, s, v]



	def converteRGB(self, hsv):
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



	def leCor(self, rgb):
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
				return 5
		else:
			if g == 1:
				return 3
			else:
				if b == 1:
					return 2
				else:
					return 1



	def verificaEntradaPraca(self):
		lista = []
		while self.sensor_direito.value() not in [6] or self.sensor_esquerdo.value() not in [6]:
			self.andarTempo(200, 200, 100)
			lista.append(self.sensor_direito.value())
			lista.append(self.sensor_esquerdo.value())

			print(lista)

			if 2 in lista: #and 4 in lista:
				self.cor_atual = 2
				self.saindoCor()
				return True

			return False



	def aprendeMapa(self, cor, atualiza = False):
		if self.mapeamento:
			self.mapa.append({cor: True})
			self.mapa_simpless.append(cor)

		if self.volta_mapa:
			self.mapa_volta.append(cor)	




	def verificaMapa(self):
		print(self.mapa_simpless, self.mapa_volta, list(reversed(self.mapa_volta)))
		if list(reversed(self.mapa_volta)) == self.mapa_simpless:
			self.volta_mapa = False
			self.mapa_volta = []
			return True
		return False



	def reverteDirecao(self):
		for i in [int(key) for key in self.cores_aprendidas.keys()]:
			self.cores_aprendidas[i] *= -1



	def voltaPraca(self):
		self.mapeamento = False
		self.volta_mapa = True
		self.reverteDirecao()
		self.bateParede()
		while True:
			self.andarTempo(400,400,100)
			self.saindoPista()

			if self.sensor_direito.value() in [3]:
				while not self.alinhaCor([3], 6, self.sensor_direito, self.sensor_esquerdo, 0, 300, True):
					continue
				break

			if self.sensor_esquerdo.value() in [3]:
				while not self.alinhaCor([3], 6, self.sensor_esquerdo, self.sensor_direito, 300, 0, True):
					continue
				break

		if self.codigoPraca(2):
			self.verificaCor(True)
			if self.codigoPraca(5):
				self.verificaCor(True)
				self.saindoCor()
				return True
		return True



	def abreGarra(self, rotation, speed, wait = False):
		self.motor_garra.run_to_rel_pos(position_sp = rotation, speed_sp = speed)
		if wait:
			self.motor_garra.wait_while('running', 2000)
		return True



	def pegaBoneco(self, garra_ocupada):
		if not garra_ocupada:
			self.motor_garra.stop()
			self.abreGarra(-100, 100, True)
			garra_ocupada = True
		return garra_ocupada



	def largaBoneco(self, garra_ocupada):
		if garra_ocupada:
			self.motor_garra.stop()
			self.abreGarra(100, 100, """True""")
			self.andarTempo(-500, -500, 100, """True""")
			self.abreGarra(-100, 100, """True""")
			self.andarTempo(500, 500, 100, """True""")
			while i < 5:
				self.abreGarra(-100, 100, True)
				self.abreGarra(100, 100, True)
				i += 1
			garra_ocupada = False
		return garra_ocupada



	def medeHipotenusaBoneco(self):
		hipotenusaBoneco = 0	
		for x in range(3):
			if self.detectaBoneco():
				hipotenusaBoneco = (self.sensor_ultrasonico.value()/10)
				self.andarRotacao(-35, -35, 50, True)
			if not self.detectaBoneco():
				self.andarRotacao(35, 35, 50, True)
		self.parar = True
		return True



	def medeHipotenusaParede(self):	
		hipotenusaParede = 0	
		if self.detectaParede():
			hipotenusaParede = (self.sensor_ultrasonico.value()/10)
			self.andarRotacao(-70, -70, 50, True)
		if not self.detectaParede():
			self.andarRotacao(70, 70, 50, True)
		return hipotenusaParede



	def modoAtaque(self):
		while not self.garra_ocupada:
			self.andarTempo(-300, -300, 200, True)
			for i in range(3):
				if not self.detectaBoneco():
					self.andarTempo(300,300,100, True)
				sleep(0.1)
			if self.detectaBoneco():
				self.medeHipotenusaBoneco()
				if self.sensor_ultrasonico.value() < 120:
					self.andarRoda("d", -40)
					self.andarRoda("e", -40)
					self.andarTempo(400, 400, 400, True)
				self.girarRobo(-90)
			else:
				self.andarTempo(-300,-300, 400, True)
				return False

			while not (self.sensor_esquerdo.value() in [0,1,7] or self.sensor_direito.value() in [0,1,7]):
				self.andarTempo(100, 100, 100)
				print(self.sensor_esquerdo.value(),self.sensor_direito.value())
			if self.sensor_esquerdo.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensor_esquerdo, self.sensor_direito, 100, 0, False, True):
					continue
			if self.sensor_direito.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensor_direito, self.sensor_esquerdo, 0, 100, False, True):
					continue
			self.girarRoda(-90)
			self.andarTempo(-200,-200,500, True)
			self.abreGarra(100,100,True)
			while not self.detectaBoneco():
				self.andarTempo(300,300,600)
			if self.detectaBoneco():
				self.medeHipotenusaBoneco()
				self.andarRotacao(220,220, 500,True)
				self.girarRobo(-90)
			sleep(0.2)
			while not (self.sensor_esquerdo.value() in [0,1,7] or self.sensor_direito.value() in [0,1,7]):
				self.andarTempo(100, 100, 100)
			if self.sensor_esquerdo.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensor_esquerdo, self.sensor_direito, 100, 0, False, True):
					continue
			if self.sensor_direito.value() in [0,1,7]:
				while not self.alinhaCor([0,1,7], 6, self.sensor_direito, self.sensor_esquerdo, 0, 100, False, True):
					continue
			self.andarTempo(-200,-200,2400, True)
			self.garra_ocupada = self.pegaBoneco(self.garra_ocupada)
			self.andarTempo(200,200,2400, True)
			self.girarRobo(90)

			if self.volta_mapa:
				self.girarRobo(180)
				self.volta_mapa = False
				self.mapa_volta = []
				self.reverteDirecao()
				return True



	def bateParede(self):
		a = 10
		d = 0
		e = 0
		bol = True
		for i in range(80):
			self.andarTempo(400, 400, 100)
			if (self.motor_esquerdo.speed < 370) and i > a:
				if self.motor_esquerdo.speed < self.motor_direito.speed:
					e += 1
					bol = False
				else:
					d += 1
					bol = False

			if (self.motor_direito.speed < 370) and i > a:
				if self.motor_esquerdo.speed < self.motor_direito.speed:
					e += 1
					bol = False
				else:
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
				a = i + 10
			if d > 3:
				self.andarTempo(-200,-200, 600, True)
				self.andarTempo(0, -300, 400, True)
				self.andarTempo(200, 200, 600, True)
				e = 0
				d = 0
				a =  i + 10
			bol = True

		return True



	def modoPraca(self, garra_ocupada):
		c = 0
		i = 0
		dist1 = 0
		dist2 = 0
		distm = 0
		hipotenusa = 0
		angulo = 0
		distpercorrida = 0
		if self.garra_ocupada:
			while self.sensor_esquerdo.value() not in [0,1,7] or self.sensor_direito.value() not in [0,1,7]:
				self.andarTempo(200,200,100)
				c = c+1
		if self.sensor_esquerdo.value() in [0,1,7]: #se o sensor tiver em preto ou marrom/unknown ele tenta alinhar
			while not self.alinhaCor([0,1,7], 6, self.sensor_esquerdo, self.sensor_direito, 100, 0, False, True):
				continue
		if self.sensor_direito.value() in [0,1,7]:
			while not self.alinhaCor([0,1,7], 6, self.sensor_direito, self.sensor_esquerdo, 0, 100, False, True):
				continue
			self.girarRobo(180)			
			self.voltar = True
			self.garra_ocupada = self.largaBoneco(self.garra_ocupada)
		while i < c-150:
			self.andarTempo(125,125,100)
			i = i + 1
		self.abreGarra(-100,100,True)
		self.girarRobo(-90)
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
			hipotenusa = self.razao_andar
			angulo = math.acos(distm/hipotenusa)*(180/math.pi)
			angulo = 90 - angulo
			girarRoda = self.girarRoda(angulo)
		else:
			distm = (dist1-dist2)
			hipotenusa = self.razao_andar
			angulo = math.acos(distm/hipotenusa)*(180/math.pi)
			angulo = 90 - angulo
			print(distm)
			girarRoda = self.girarRoda(-angulo)
			self.andarTempo(100,100,100,True)
		while self.detectaParede():
			self.andarTempo(100,100,100)
		if not self.detectaParede():
			self.andarTempo(75,75,100)
			self.girarRobo(90)
		return True