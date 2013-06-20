##################################
#
# clpopulation.py
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
import sys
import clneurons

class clpopulation:
	def __init__(self, object="population", attr={}):
		self.object = object
		self.name = "****"
		if attr.get("name"): self.name=attr["name"]
		self.workobj=None
		#### Neurons projection mechanisms.
		self.op = []
		self.connections ={}
		#### List of neurons
		self.neurons=[]
		self.__neurons=[]
		#### Time to next spike
		self.timetospike = []
		self.number = 0
	def startpoint(self,object,attr):
		if self.workobj != None:
			self.workobj.startpoint(object,attr)
		elif object == "neurons" and self.workobj == None:
			self.workobj = clneurons.clneurons(attr=attr)
			self.__neurons.append( self.workobj )
			self.workobj.connections = self.connections
		else:
			sys.stderr.write("Unexpected tag in <population> expression: %s\nABBORT\n\n"%object);
			sys.exit(1)
	def stoppoint(self, object):
		if self.workobj != None and object != "neurons":
			self.workobj.stoppoint(object)
		elif self.workobj != None and object == "neurons":
			self.op = reduce(lambda y,x:y+x.op, self.__neurons, [])
			self.timetospike = reduce(lambda y,x:y+x.timetospike, self.__neurons, [])
			self.number = reduce(lambda x,y:x+y.number,self.__neurons, 0)
			self.workobj = None
		else:
			sys.stderr.write("Unexpected close tag <%s> in <population> expression\nABBORT\n\n"%object);
			sys.exit(1)
	def write(self):
		result=["<population name=\"%s\" number=\"%d\">"%(self.name, self.number)]
		for nrn in self.__neurons:
			for lines in nrn.write():
				result.append("\t"+lines)
		result.append("</population>")
		return result
	def getnames(self):
		result = []
		for nrn in self.__neurons:
			for prn in nrn.getnames():
				result.append( self.name+":"+prn )
		return result
	def update(self,model):
		for nrn in self.__neurons: nrn.update(model)
		self.op = reduce(lambda y,x:y+x.op, self.__neurons, [])
	def calculate(self,model):
		for nrn in self.__neurons: nrn.calculate(model)
		self.timetospike = reduce(lambda y,x:y+x.timetospike, self.__neurons, [])
		self.neurons =  reduce(lambda y,x:y+x.neurons, self.__neurons, [])
		
		
