##################################
#
# engine.py
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
import clmodel
import modelparcer as mp
from xml.sax import make_parser
import os
import sys
import threading as td
class engine(td.Thread):
	def __init__(self, filename = None, mode = "STD"):
		td.Thread.__init__(self)
		global model
		if filename == None:
			sys.stderr.write("Wrong filename\nABBORT\n\n");
			sys.exit(1)
		parser=make_parser()
		parser.setContentHandler(mp.modelparcer())
		parser.parse(filename)
		mp.model.mode = mode
		self.model = mp.model
	def write(self,filename=None):
		global model
		if filename == None:
			sys.stderr.write("Cannt write ot None\nABBORT\n\n");
			return
		fd = open(filename, "w")
		for prn in mp.model.write():
			fd.write(prn + "\n")
	def run(self):
		self.model.run()
		


if __name__ == '__main__' :
	if len(sys.argv) == 1:
		print "USAGE: %s [OPTIONS] modelfile.xml" % sys.argv[0]
		sys.exit(1)
	egn = engine(filename=sys.argv[-1])
	egn.run()
	print "ok!"

