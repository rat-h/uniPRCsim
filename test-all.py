##################################
#
# test-all.py
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
from xml.sax import make_parser
import modelparcer as mp

global model


print "<!-- TEST MODEL-PARSER CLASS --->"
parser=make_parser()
parser.setContentHandler(mp.modelparcer())
parser.parse("example.xml")
print "<!---------- HAS DONE ----------->\n\n"

print "<!-- TEST PRC CLASS --->"
print  "<!-- Type I --->"
p = mp.model.objlst["prc"]["Type I"]
for i in  p.write():
	print i
for test_item in ( (0.2,0.0), (0.2,1.0),(0.2,0.1), (0.1,0.15), (0.25,0.2), (0.15,0.2),
					(0.0,0.2), (0.1,1.2)):
	rst = p.getvl(test_item[0], test_item[1])
	print "gsyn=%g, ph=%g :"% test_item, float(rst[0])," :",float(rst[1])

print "\n<!-- Type II --->"
p = mp.model.objlst["prc"]["Type II"]
for i in  p.write():
	print i
for test_item in ( (0.2,0.1), (0.1,0.15), (0.25,0.2), (0.15,0.2),
					(0.2,0.9), (0.0,0.9),(0.15,-0.9)):
	rst = p.getvl(test_item[0], test_item[1])
	print "gsyn=%g, ph=%g :"% test_item, float(rst[0])," :",float(rst[1])

print "<!---------- HAS DONE ----------->\n\n"

print "<!-- TEST MODEL CLASS --->"
print "<simulation maxspikes=\"%d\" />" % mp.model.maxspikes
for fl in mp.model.objlst["outputs"]:
	print "<output name=\"%s\" format=\"%s\" watch=\"%s\" />"%(fl.name,fl.format,fl.watch)
print "<!---------- HAS DONE ----------->\n\n"

print "<!-- TEST POPULATION CLASS --->"
for popul in mp.model.objlst["neurons"].items():
	print "<!-- Name: %s(%s): Number of subobjects: %d --->"%(popul[0],popul[1].name,len(popul[1].neurons) )
	for prn in popul[1].write():
		print prn
print "<!---------- HAS DONE ----------->\n\n"

print "<!-- TEST CONNECTION CLASS --->"
for con in mp.model.objlst["connections"].items():
	print con[1].write()
print "<!---------- HAS DONE ----------->\n\n"

print "<!-- TEST CONNECTIVITY --->"
for popul in mp.model.objlst["neurons"].items():
	print "<!-- Name: %s(%s): input connections --->"%(popul[0],popul[1].name)
	for connect in popul[1].connections.items():
		print "\t<connections>"
		for con in connect[1]:
			print "\t\t<connect name=\"%s\" form=\"%s\" prc=\"%s\" gsyn=\"%g\" delay=\"%g\" jitter=\"%g\" />"%(
				con.name, con.frm.name, con.prc.name, con.gsyn,
				con.delay, con.jitter
			)
		print "\t<connections>"
print "<!---------- HAS DONE ----------->\n\n"
mp.model.run()
