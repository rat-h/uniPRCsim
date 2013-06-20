##################################
#
# clnoisyneurons.py
# Copyright (C) Louisiana State University, Health Sciences Center
# Written by 2011-2013 Ruben Tikidji-Hamburyan <rth@nisms.krinc.ru>
#                  
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, GOOD TITLE or
# NON INFRINGEMENT.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
###################################
import random as rnd
import string
import sys
import math
#########################################################
# process:
# 0 - OUP
# 1 - Feller
# 2 - Period Additive noise
# 3 - Phase Additive noise
# 4 - OUP + resetting
# 5 - Feller + resetting
#########################################################

class clnoisyneurons:
	def __init__(self, object="noisyneurons", attr={}):
		#### Default paramters
		self.number = 1
		self.period_mu  = 1
		self.period_sd  = 1
		self.period_tau = 1
		self.name="*****"
		self.object=object
		self.saturation = -1
		self.process = 0 #0 - OU, 1 - Feller, 2 - OU+PRC, 3 - Feller+PRC
		self.f2='summ'
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "number": continue
			if atr == "period_mu": continue
			if atr == "period_sd": continue
			if atr == "period_tau": continue
			if atr == "process": continue
			if atr == "name": continue
			if atr == "f2": continue
			sys.stderr.write("Unexpected attribut \'%s\'for tag <neurons>\nABBORT\n\n"%atr)
			sys.exit(1)

		#### Reset from attrebuts
		if attr.get("number"):	self.number = int( attr["number"] )
		if attr.get("period_mu"):	self.period_mu = float( attr["period_mu"] )
		if attr.get("period_sd"):	self.period_sd = float( attr["period_sd"] )
		if attr.get("period_tau"):	self.period_tau = float( attr["period_tau"] )
		if attr.get("process"):	self.process = int( attr["process"] )
		if attr.get("name"):	self.name = attr["name"]
		if attr.get("f2"):		self.f2 = attr["f2"]
		#Array of neurons the numbers are
		#	phase, second order correction and last period
		self.neurons = [ [0, 0, 0] for x in xrange(self.number) ]
		if self.process != 3:
			self.periods = [  rnd.gauss(self.period_mu,self.period_sd) for x in xrange(self.number) ]
		else :
			self.periods = [  self.period_mu for x in xrange(self.number) ]
		self.timetospike = [ 0 for x in xrange(self.number) ]
		#### Dic of named connections
		self.connections = {}
		#### Output buffers
		self.op = [ 0 for x in xrange(self.number) ]
		self.__lastspike = [ 0 for x in xrange(self.number) ]
	def startpoint(self,object,attr):
		if object == "init" :
			if attr.get("ph0_all") :
				for i in xrange(self.number):
					self.neurons[i][0] = float(attr["ph0_all"])
			if attr.get("ph1_all") :
				for i in xrange(self.number):
					self.neurons[i][1] = float(attr["ph1_all"])
			if attr.get("ph0_all") and attr.get("ph0_sd") :
				for i in xrange(self.number):
					self.neurons[i][0] = rnd.normalvariate(
						float(attr["ph0_all"]), float(attr["ph0_sd"])
						)
					if self.neurons[i][0] > 1.0: self.neurons[i][0] -= abs( math.floor(self.neurons[i][0]) ) + 1.0
			if attr.get("ph1_all") and attr.get("ph1_sd") :
				for i in xrange(self.number):
					self.neurons[i][1] = rnd.normalvariate(
						float(attr["ph1_all"]), float(attr["ph1_sd"])
						)
					if self.neurons[i][1] > 1.0: self.neurons[i][1] -= abs( math.floor(self.neurons[i][1]) ) + 2.0
			if attr.get("ph0"):
				setstrl=string.split(attr["ph0"],",")
				if len(setstrl) < self.number:
					for i in xrange(len(setstrl)):
						self.neurons[i][0] = float( setstrl[i] )
				else :
					for i in xrange(self.number):
						self.neurons[i][0] = float( setstrl[i] )
			if attr.get("ph1"):
				setstrl=string.split(attr["ph1"],",")
				if len(setstrl) < self.number:
					for i in xrange(len(setstrl)):
						self.neurons[i][1] = float( setstrl[i] )
				else :
					for i in xrange(self.number):
						self.neurons[i][1] = float( setstrl[i] )
			
			for i in xrange(self.number):
				self.timetospike[i] = self.periods[i]*(1.0 - self.neurons[i][0])
			
		elif object == "saturation":
			return
		else:
			sys.stderr.write("Unexpected tag <%s> in <neuron> expression\nABBORT\n\n"%object);
			sys.exit(1)

	def stoppoint(self, object):
		if object == "neuron" or object == "init" or object == "saturation":
			return
		else:	
			sys.stderr.write("Unexpected close tag <%s> in <neurons> expression\nABBORT\n\n"%object);
			sys.exit(1)
	def write(self):
		result=["<noisyneurons name=\"%s\" number=\"%d\" period_mu=\"%g\" period_sd=\"%g\" period_tau=\"%g\" process=\"%d\">"%(self.name, self.number, self.period_mu, self.period_sd, self.period_tau, self.process)]
		for i in xrange(self.number):
			result.append(
				"\t <condition ph=\"%g\" correction=\"%g\" timetospike=\"%g\" />"
				% (self.neurons[i][0],self.neurons[i][1],self.timetospike[i])
			)
		result.append("</noisyneurons>")
		return result
	def getnames(self):
		result = []
		for cnt in xrange(self.number):
			result.append("%s:%d"%(self.name,cnt+1))
		return result
		
	def calculate(self,model):
		for cont in self.connections.items():
			gsyn_sum = 0
			for con in cont[1]:
				gsyn_sum += con.gsyn * reduce(lambda x,y:x+y, con.op)
			for nrn in xrange(self.number):
				#Insert here saturation code!
				#----------------------------
				correction = cont[1][0].prc.getvl( gsyn_sum, self.neurons[nrn][0])
				if self.process < 3:
					self.neurons[nrn][0] -= correction[0]	#f1 contribution (why - ?)
				elif self.process == 3:
					
					self.neurons[nrn][0] -= correction[0] + rnd.gauss(0,self.period_sd)
					if self.neurons[nrn][0] > 1: self.neurons[nrn][0] = 1
				else:
					sys.stderr.write("Name:%s; #:%d; Process:%d; P[n]=%g; ph[n]=%g; cor=%g; =="%(self.name,nrn,self.process,self.periods[nrn],self.neurons[nrn][0], correction[0]) )
					if self.process == 4:
						self.periods[nrn] += (self.period_mu - self.periods[nrn]) * model.timetospike/self.period_tau + rnd.gauss(0,self.period_sd) * math.sqrt(model.timetospike) + correction[0] * self.periods[nrn]
					else: # process == 5
						self.periods[nrn] += (self.period_mu - self.periods[nrn]) * model.timetospike/self.period_tau + rnd.gauss(0,self.period_sd) * math.sqrt(self.periods[nrn]*model.timetospike) + correction[0] * self.periods[nrn]
					pln = (self.period_tau*self.periods[nrn]-(self.period_mu-self.periods[nrn])*(model.elapsed_time - self.__lastspike[nrn]))/(self.period_tau+self.periods[nrn]+self.period_mu)
					self.neurons[nrn][0] = (model.elapsed_time - self.__lastspike[nrn])/pln
					#self.neurons[nrn][0] = (model.elapsed_time - self.__lastspike[nrn])/self.periods[nrn]
					sys.stderr.write("=> P[n+1]=%g; ph[n+1]=%g tos=%g\n"%(self.periods[nrn],self.neurons[nrn][0],self.periods[nrn] * (1.0 - self.neurons[nrn][0])) )
				if self.f2 == "off": continue
				elif self.f2 == "last":
					self.neurons[nrn][1] = correction[1]	#replace f2 contribution
				else :
					self.neurons[nrn][1] += correction[1]	#accumulate  f2 contribution
		for nrn in xrange(self.number):
			self.timetospike[nrn] = self.periods[nrn] * (1.0 - self.neurons[nrn][0])
			### RK2 ????
			###self.timetospike[nrn] = self.periods[nrn] * (1.0 - self.neurons[nrn][0])
	def update(self,model):
		for nrn in xrange(self.number):
			if self.process >= 4:
				sys.stderr.write("mintos:%e; tos:%e; diff:%d\n"%(model.timetospike,self.timetospike[nrn],self.timetospike[nrn] <= model.timetospike))
			if (self.timetospike[nrn] - model.timetospike) < 1e-7:
				if self.process >= 4: sys.stderr.write("SPIKE\n")
				self.op[nrn] = 1
				self.neurons[nrn][0] = 0.0
				if self.f2 != "off":
					self.neurons[nrn][0] -= self.neurons[nrn][1]
					self.neurons[nrn][1] = 0.0
				self.neurons[nrn][2] = model.elapsed_time - self.__lastspike[nrn]
				self.__lastspike[nrn] = model.elapsed_time
				if self.process == 0 or self.process == 4:
					# Deterministic part
					self.periods[nrn] += (self.period_mu - self.periods[nrn]) * (1.0 - math.exp( - self.neurons[nrn][2]/self.period_tau) )
					# Stochastic part
					self.periods[nrn] += math.sqrt(self.period_sd*self.period_tau/2*(1-math.exp(-2*self.periods[nrn]/self.period_tau)))*rnd.gauss(0,1.0)
					#while self.periods[nrn] <= 0.0 :
					#	self.periods[nrn] += (self.period_mu - self.periods[nrn]) * (1.0 - math.exp( - self.neurons[nrn][2]/self.period_tau) ) + rnd.gauss(0,self.period_sd) * math.sqrt(self.neurons[nrn][2])
				elif self.process == 1 or self.process == 5:
					self.periods[nrn] += (self.period_mu - self.periods[nrn]) * (1.0 - math.exp( - self.neurons[nrn][2]/self.period_tau) ) + rnd.gauss(0,self.period_sd) * math.sqrt(self.periods[nrn]*self.neurons[nrn][2])
					#while self.periods[nrn] <= 0.0 :
					#	self.periods[nrn] += (self.period_mu - self.periods[nrn]) * (1.0 - math.exp( - self.neurons[nrn][2]/self.period_tau) ) + rnd.gauss(0,self.period_sd) * math.sqrt(self.periods[nrn]*self.neurons[nrn][2])
				elif self.process == 2:
					self.periods[nrn] = rnd.gauss(self.period_mu,self.period_sd)
			else:
				if self.process == 3:
					self.neurons[nrn][0] += model.timetospike/self.periods[nrn] + rnd.gauss(0,self.period_sd)
					if self.neurons[nrn][0] > 1: self.neurons[nrn][0] = 1
				else: # 0 1 2 4 5
					self.neurons[nrn][0] += model.timetospike/self.periods[nrn]
				self.op[nrn] = 0


