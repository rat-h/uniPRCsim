from xml.sax import handler
import string
import math, sys
import clmodel

		
class modelparcer(handler.ContentHandler):
	def __init__(self):
		self.objlst={}
		self.workobj=None
	def startElement(self, name, attr):
		global model
		if name =="model":
			self.workobj = clmodel.clmodel(name,attr)
			if not self.objlst.get("model", 0):
				self.objlst["model"]={}
			self.objlst["model"][name]= self.workobj
			model = self.workobj
		elif self.workobj != None:
			self.workobj.startpoint(name,attr)
		else:
			sys.stderr.write("Unexpected tag in root XML instant: %s\nABBORT\n\n"%name);
			sys.exit(1)
		
	def endElement(self, name):
		if name =="model" and self.workobj != None:
			self.workobj = None
		elif self.workobj != None:
			self.workobj.stoppoint(name)
		else:
			sys.stderr.write("Unexpected close tag <%s> in XML root\nABBORT\n\n"%name);
			sys.exit(1)
		
		
