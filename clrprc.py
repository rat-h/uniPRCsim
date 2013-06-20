##################################
#
# clrprc.py
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
		if find != None: self.prc = find(object="prc",name=attr["prc"])
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
		if gsyn <= 0.0: return(0.0, 0.0)
		mu = self.prc.getvl(gsyn, ph)
		reset1 = rnd.normalvariate(mu[0],self.sd)
		while reset1 < (ph - 1.0):
			reset1 = rnd.normalvariate(mu[0],self.sd)
		return (
			reset1,
			rnd.normalvariate(mu[1],self.sd2)
			)
