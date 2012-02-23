import random as rnd
import string
import sys

class clneurons:
	def __init__(self, object="neurons", attr={}):
		#### Default paramters
		self.number = 1
		self.period = 1
		self.name="*****"
		self.object=object
		self.saturation = -1
		self.f2='summ'
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "number": continue
			if atr == "period": continue
			if atr == "name": continue
			if atr == "f2": continue
			sys.stderr.write("Unexpected attribut \'%s\'for tag <neurons>\nABBORT\n\n"%atr)
			sys.exit(1)

		#### Reset from attrebuts
		if attr.get("number"):	self.number = int( attr["number"] )
		if attr.get("period"):	self.period = float( attr["period"] )
		if attr.get("name"):	self.name = attr["name"]
		if attr.get("f2"):		self.f2 = attr["f2"]
		#Array of neurons the numbers are
		#	phase, second order correction and	last period
		self.neurons = [ [0, 0, 0] for x in xrange(self.number) ]
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
				self.timetospike[i] = self.period*(1.0 - self.neurons[i][0])
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
		result=["<neurons name=\"%s\" number=\"%d\" period=\"%g\">"%(self.name, self.number, self.period)]
		for i in xrange(self.number):
			result.append(
				"\t <condition ph=\"%g\" correction=\"%g\" timetospike=\"%g\" />"
				% (self.neurons[i][0],self.neurons[i][1],self.timetospike[i])
			)
		result.append("</neurons>")
		return result
	def getnames(self):
		result = []
		for cnt in xrange(self.number):
			result.append("%s:%g"%(self.name,cnt+1))
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
				#print self.name,": gsum:",gsyn_sum, "phi:",self.neurons[nrn][0], " ==>", correction,
				self.neurons[nrn][0] -= correction[0]	#f1 contribution (why - ?)
				#print "phi:", self.neurons[nrn][0]
				if self.f2 == "off": continue
				elif self.f2 == "last":
					self.neurons[nrn][1] = correction[1]	#replace f2 contribution
				else :
					self.neurons[nrn][1] += correction[1]	#replace f2 contribution
		for inx in xrange(self.number):
			#print self.name,": phi:",self.neurons[inx][0], "tos:",self.timetospike[inx],
			self.timetospike[inx] = self.period * (1.0 - self.neurons[inx][0])
			#print "===>",self.timetospike[inx]
	def update(self,model):
		for inx in xrange(self.number):
			if self.timetospike[inx] <= model.timetospike:
				self.op[inx] = 1
				self.neurons[inx][0] = 0.0
				if self.f2 != "off":
					self.neurons[inx][0] -= self.neurons[inx][1]
					self.neurons[inx][1] = 0.0
				self.neurons[inx][2] = model.elapsed_time - self.__lastspike[inx]
				self.__lastspike[inx] = model.elapsed_time
			else:
				self.neurons[inx][0] += model.timetospike/self.period
				self.op[inx] = 0
		

