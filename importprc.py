import sys
import os
import csv
import string as str
import re
import glprc
from xml.sax import handler, make_parser

class prcparcerpxm(handler.ContentHandler):
	def __init__(self,mode = "export", name = None):
		self.prclst=[]
		self.mode = mode
		self.prc = None
		self.prcfl = False
		self.name = name
	def startElement(self, name, attr):
		if name =="prc":
			if self.prcfl: return
			if self.mode == "list" and attr.get("name", 0):
				self.prclst.append(attr["name"])
				return
			if attr.get("name", 0) == 0 or self.name == None or attr["name"] != self.name:
				return
			self.prcfl = True
			self.prc = glprc.odprc()
			self.prc.name = attr["name"]
			self.prc.gsyn = attr["gsyn"]
			return
		if name == "item" and self.prcfl:
			if not attr.get("ph",0): return
			if not attr.get("prc1",0): return
			if attr.get("prc2",0):
				self.prc.data.append([attr["ph"], str.split(attr["prc1"],','), str.split(attr["prc2"],',') ] )
				self.prc.f1 = True
			else:
				self.prc.data.append([attr["ph"], str.split(attr["prc1"],','), [] ] )
				self.prc.f2 = False
			
		
	def endElement(self, name):
		if name =="prc":
			self.prcfl = False
		

class importprc:
	def __init__(self):
		self.name="..."
		self.gsyn=None
		self.data={}
	def readxml(self,filename):
		pparser = prcparcerpxm(name=self.name)
		parser=make_parser()
		parser.setContentHandler(pparser)
		parser.parse(filename)
		self.gsyn = pparser.prc.gsyn
		for data in pparser.prc.data:
			if not self.data.get(data[0], 0):
				self.data[ data[0] ]=[ data[1],data[2] ]
			
	def readfile(self,filename,format="excel-tab",fx="1"):
		if format == "pxm" : return self.readxml(filename)
		fd = open(filename, "r")
		data = csv.reader(fd,dialect=format)
		for row in data:
			if len(row) == 0: continue
			elif len(row) > 1:
				nrow = row
			else:
				nrow = row[0].split()
#			print row, " -> ", nrow
			if not self.data.get(nrow[0], 0):
				self.data[ nrow[0] ]=[ [],[] ]
			if fx == '1':
				self.data[ nrow[0] ][0].append(nrow[1])
			else:
				self.data[ nrow[0] ][1].append(nrow[1])
		fd.close()
		return
	def close(self):
		list=[]
		for item in self.data.items():
			if len(item[1][0]) != len(item[1][1]) and len(item[1][1]) != 0:
				sys.stderr.write("Two different prc1 and prc2 at ph=%s\nAbbort\n\n"%item[0])
				sys.exit(1)
		for item in self.data.items():
			list.append(item)
		list.sort()
		self.data=list
	def write(self):
		result=["<prc name=\"%s\" gsyn=\"%s\">"%(self.name, self.gsyn)]
		for item in self.data:
			if len(item[1][1]) == 0:
				result.append("\t<item ph=\"%s\" prc1=\"%s\" />"%(
					item[0], str.join(item[1][0]).replace(" ",",") )
				)
			else:
				result.append("\t<item ph=\"%s\" prc1=\"%s\" prc2=\"%s\"/>"%(
					item[0], str.join(item[1][0]).replace(" ",","),
					str.join(item[1][1]).replace(" ",",") )
				)
		result.append("</prc>")
		return result
	def getodprc(self):
		result = glprc.odprc()
		result.name, result.gsyn = self.name, self.gsyn
		for item in  self.data.items():
			result.data.append( [float(item[1][0]),[],[] ] )
			returlt.data[-1][1] = map( float, item[1][1])
			returlt.data[-1][2] = map( float, item[1][2])
		result.data.sort()
		return result
	def getglprc(self):
		result = glprc.odprc()
		result.name, result.gsyn = self.name, self.gsyn
		result.data = []
		for item in  self.data.items():
			result.data.append( [item[0],item[1][0],item[1][1]] )
		result.data.sort()
		#print result.data
		if result.data[0][2] != []:
			result.f2 = True
		return result
	def clear(self):
		del self.data
		self.data = {}



if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "USAGE: %s prc-name gsyn f1-datafile [f2-datafila]" % sys.argv[0]
		sys.exit(1)

	impprc = importprc()
	impprc.name = sys.argv[1]
	impprc.gsyn = sys.argv[2]
	for fname in str.split(sys.argv[3]):
		impprc.readfile(fname)
	if len(sys.argv) > 4:
		for fname in str.split(sys.argv[4]):
			impprc.readfile(fname,fx='2')
	impprc.close()
	for i in impprc.write():
		print "\t%s"%i
			
