import random as rnd
import sys

class clconnection:
	def __init__(self, find=None,object="connection",attr={}):
		#### Default paramters
		self.object	= object
		self.name	= "*****"
		self.frm	= None
		self.to		= None
		self.prc	= None
		self.gsyn	= 0.0
		self.delay	= -1
		self.jitter	= -1
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "name": continue
			if atr == "prc": continue
			if atr == "from": continue
			if atr == "to": continue
			if atr == "gsyn": continue
			if atr == "delay": continue
			if atr == "jitter": continue
			sys.stderr.write("Unexpected attribut \'%s\'for tag <connection>\nABBORT\n\n"%atr)
			sys.exit(1)
		#### Reset attrebuts
		if attr.get("name"):	self.name = attr["name"]
		if attr.get("prc"):
			self.prc = find("prc", attr["prc"])
		if attr.get("from"):
			self.frm = find("neurons", attr["from"])
		if attr.get("to"):
			self.to = find("neurons", attr["to"])
		if attr.get("gsyn",0) != 0:
			self.gsyn = float( attr["gsyn"] )
		if attr.get("delay",0 ) != 0:
			self.delay = float( attr["delay"] )
		if attr.get("jitter",0) != 0:
			self.jitter = float( attr["jitter"] )
		if self.prc == None or self.frm == None or self.to == None or self.gsyn < 0.0:
			sys.stderr.write("Uncomplited tag <connection>\nShould containes frm=, to=, prc= and gsyn= atributes\nABBORT\n\n")
			sys.exit(1)
		### Iner paramters
		self.fifo	= [ [] for x in xrange( self.frm.number) ]
		### I/O parameters
		self.timetospike = self.frm.timetospike
		if self.delay > 0:
			self.timetospike = [ x+self.delay for x in self.frm.timetospike]
		self.op = [ 0 for x in xrange( self.frm.number) ]
		#### Connect to target
		if not self.to.connections.get( attr["prc"], 0 ):
			self.to.connections[attr["prc"]] = []
		self.to.connections[attr["prc"]].append(self)
	def startpoint(self,object,attr={}):
		sys.stderr.write("Unexpected tag in <connection> expression: %s\nABBORT\n\n"%object);
		sys.exit(1)
	def stoppoint(self, object):
		sys.stderr.write("Unexpected close tag <%s> in <connection> expression\nABBORT\n\n"%object);
		sys.exit(1)
	def write(self):
		return ["<connection name=\"%s\" from=\"%s\" to=\"%s\" prc=\"%s\" gsyn=\"%g\" delay=\"%g\" jitter=\"%g\" />"%(
			self.name, self.frm.name, self.to.name, self.prc.name, self.gsyn, self.delay, self.jitter
		)]
	def getnames(self):
		return [ self.name ]
	def update(self, model):
		if self.delay <= 0.0:
			self.op = self.frm.op
			return
		for idx in xrange(self.frm.number):
			if self.timetospike[idx] <= model.timetospike:
				self.op[idx] = 1
				self.fifo[idx].pop(0)
			else :
				self.op[idx] = 0
			if self.frm.op[idx] == 1:
				self.fifo[idx].append(-1.0)
#		print "TOS for %s: "%self.name, self.timetospike
#		print "FIFO for %s: "%self.name, self.fifo," before uodate!"
	def calculate(self, model):
		if self.delay <= 0.0:
			self.timetospike = self.frm.timetospike
		else:
			for idx in xrange(self.frm.number):
				for tdx in xrange( len(self.fifo[idx]) ):
					if self.fifo[idx][tdx] < 0.0:
						self.fifo[idx][tdx] = 0.0
					else:
						self.fifo[idx][tdx] += model.timetospike/self.delay
				
				if len(self.fifo[idx]) == 0:
					self.timetospike[idx] = 1e19
				else:
					if self.jitter > 0.0:
						ndelay = rnd.normalvariate(self.delay, self.jitter)
						self.timetospike[idx] = ndelay * (1 - self.fifo[idx][0])
						sys.stderr.write("JITTER:%g === (%g) ===> %g\n"%(self.delay,self.jitter,ndelay))
						#self.timetospike[idx] = rnd.normalvariate(self.delay, self.jitter) * (1 - self.fifo[idx][0])
					else:
						self.timetospike[idx] = self.delay * (1 - self.fifo[idx][0])

