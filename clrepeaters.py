##################################
#
# clneurons.py 
# Copyright (C) Louisiana State University, Health Sciences Center
# Written by 2011-2014 Ruben Tikidji-Hamburyan <rth@nisms.krinc.ru>
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
import sys,math

class clrepeaters:
	def __init__(self, object="repeaters", attr={}):
		#### Default paramters
		self.number = 1
		self.slope = 0 #a
		self.offset = 1 #b
		self.name="*****"
		self.object=object
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "offset": continue
			if atr == "name": continue
			if atr == "slope": continue
			if atr == "min": continue
			sys.stderr.write("Unexpected attribute \'%s\'for tag <repeaters>\nABORT\n\n"%atr)
			sys.exit(1)

		#### Reset from attrebuts
		if attr.get("slope"):	self.slope = float( attr["slope"] )
		if attr.get("name"):	self.name = attr["name"]
		if attr.get("offset"):	self.offset = float(attr["offset"])
		if attr.get("min"):	self.min = float( attr["min"] )
		else:			self.min = 0.
		#Array of neurons the numbers are
		#	phase, second order correction and	last period
		self.neurons = [ [0, 0, 0]  ]
		self.timetospike = [ 1e19  ]
		#### Dic of named connections
		self.connections = {}
		#### Output buffers
		self.op = [ 0 ]
		self.period = 1e19
		self.__lastspike =  0.
	def startpoint(self,object,attr):
		sys.stderr.write("Unexpected tag <%s> in <repeaters> expression\nABBORT\n\n"%object);
		sys.exit(1)

	def stoppoint(self, object):
		if object == "repeaters": #or object == "init" or object == "saturation":
			return
		else:	
			sys.stderr.write("Unexpected close tag <%s> in <repeaters> expression\nABBORT\n\n"%object);
			sys.exit(1)
	def write(self):
		result=["<repeaters name=\"%s\" offset=\"%g\" slope=\"%g\"/>"%(self.name, self.offset, self.slope)]
		return result
	def getnames(self):
		result = []
		for cnt in xrange(self.number):
			result.append("%s:%g"%(self.name,cnt+1))
		return result
		
	def calculate(self,model):
		prespike  = 0
		for cont in self.connections.items():
			for con in cont[1]:
				prespike += reduce(lambda x,y:x+y, con.op, 0)
		if prespike > 0:
			#DB>>
			#print prespike,"slope:",self.slope,"offset:",self.offset,"x:",model.elapsed_time - self.__lastspike,"({},{})".format(model.elapsed_time,self.__lastspike),"==>",
			#<<DB
			tmp = (model.elapsed_time - self.__lastspike) 
			self.timetospike = [ tmp * self.slope + self.offset if tmp > self.min else self.min ]
		#DB>>
		#print self.timetospike
		#<<DB

	def update(self,model):
		if self.timetospike[0] <= model.timetospike:
			self.op[0] = 1
			self.neurons[0][2] = model.elapsed_time - self.__lastspike
			self.__lastspike = model.elapsed_time
			self.timetospike = [ 1e19 ]
		else:
			self.op[0] = 0
		

