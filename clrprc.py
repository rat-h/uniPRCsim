import random as rnd
import sys
import clprc

class clrprc:
	def __init__(self,object="rprc",find=None, attr={}):
		self.object	=object,
		self.name	="*****"
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "prc": continue
			if atr == "sd": continue
			if atr == "name": continue
			if atr == "sd2": continue
			sys.stderr.write("Unexpected attribut \'%s\'for tag <output>\nABBORT\n\n"%atr)
			sys.exit(1)

		if attr.get("name"):
			self.name	= attr["name"]
		if not attr.get("prc",0):
			sys.stderr.write("Uncomplited tag <rprc>\nShould containes prc= atributes\nABBORT\n\n");
			sys.exit(1)
		self.prc = find(object="prc",name=attr["prc"])
		if attr.get("sd"):
			self.sd = float(attr["sd"])
		else:
			sys.stderr.write("Uncomplited tag <rprc>\nShould containes sd= atributes\nABBORT\n\n");
			sys.exit(1)
		if attr.get("s2"):
			self.sd2 = float(attr["sd2"])
		else:
			self.sd2 = self.sd
	def startpoint(self,object,attr={}):
		sys.stderr.write("Unexpected tag in <rprc> expression: %s\nABBORT\n\n"%object);
		sys.exit(1)
	def stoppoint(self, object):
		#if object == "rprc": return
		sys.stderr.write("Unexpected close tag <%s> in <rprc> expression\nABBORT\n\n"%object);
		sys.exit(1)
	def write(self):
		return ["<rprc name=\"%s\" prc=\"%s\" sd=\"%g\" sd2=\"%g\" />"%(
			self.name, self.prc.name, self.sd, self.sd2)]
	def getvl(self, gsyn, ph):
#		sys.stderr.write("getvl:")
		mu = self.prc.getvl(gsyn, ph)
		return (
			rnd.normalvariate(mu[0],self.sd),
			rnd.normalvariate(mu[1],self.sd2)
			)
			
