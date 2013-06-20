##################################
#
# modelparcer.py
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
		
		
