##################################
#
# uniprcsimversion.py
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

MAJOR=0
MINOR=0
PATCH=42
DATE="20130620"
def getversion():
	return "%d.%02d.%04d"%(MAJOR,MINOR,PATCH)
def getlongversion():
	#TODO: add here some information
	return "uniPRCsim version %d.%02d.%04d (%s)"%(MAJOR,MINOR,PATCH,DATE)


if __name__ == "__main__":
	import time, re, os, sys
	DATE = time.strftime("%Y%m%d",time.localtime())
	fdr = open ("uniprcsimversion.py", "r")
	fdw = open ("nuniprcsimversion.py", "w")
	for line in fdr.readlines():
		fdw.write( re.sub("^DATE=\"\\d*\"","DATE=\"%s\""%DATE, line ) ) 
	fdr.close()
	fdw.close()
	os.rename("nuniprcsimversion.py","uniprcsimversion.py")
	import uniprcsimversion

	if 	os.system("zip -9 uniPRCsim-update%s.z *.py"%getversion()):
		sys.stderr.write("Cannot create zip file\n\n")
		sys.exit(1)
	if os.system("git commit -a"):
		sys.stderr.write("Cannot commit current version\n\n")
		sys.exit(1)
	if os.system("git tag \\\"v%s\\\""%getversion()):
		sys.stderr.write("Cannot tag current version\n\n")
		sys.exit(1)
	PATCH += 1
	fdr = open ("uniprcsimversion.py", "r")
	fdw = open ("nuniprcsimversion.py", "w")
	for line in fdr.readlines():
		fdw.write( re.sub("^PATCH=\\d*", "PATCH=%d"%PATCH,line ) )
	fdr.close()
	fdw.close()
	os.rename("nuniprcsimversion.py","uniprcsimversion.py")
