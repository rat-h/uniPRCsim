import string
import math
import sys

class clprc:
	def __init__(self, object="prc",  attr={}):
		self.object=object
		#### Test for implicit attributes:
		for atr in attr.keys():
			if atr == "name": continue
			if atr == "gsyn": continue
			sys.stderr.write("Unexpected attribut \'%s\'for tag <prc>\nABBORT\n\n"%atr)
			sys.exit(1)
		if not attr.get("name",0):
			sys.stderr.write("Wrong format <prc> tag: Cannot find   \'name\' attribute\nABBORT\n\n");
			sys.exit(1)
		self.name=attr["name"]
		if not attr.get("gsyn",0):
			sys.stderr.write("Wrong format <prc> tag: Cannot find   \'gsyn\' attribute\nABBORT\n\n");
			sys.exit(1)
		#### List of synaptic conductances
		self.header=[]
		#### List of PRC data
		self.data=[]
		#### Read least of synaptic condutances
		self.readheader(attr["gsyn"])
	def startpoint(self,name,attr):
		if name =="item":
			if not attr.get("prc2", 0):
				self.readitem(float(attr["ph"]),attr["prc1"]);
			else :
				self.readitem(float(attr["ph"]),attr["prc1"], attr["prc2"])
		else:
			sys.stderr.write("Unexpected tag in <prc> instant: %s\nABBORT\n\n"%name);
			sys.exit(1)
			
	def stoppoint(self,name):
		return
	def readheader(self, header):
		setstr=string.split(header,",")
		if len(setstr) < 1:
			return 1
		self.header=[0]
		for item in setstr:
			self.header.append(float(item))
	def readitem(self, ph, dat1, dat2=""):
		setstr1=string.split(dat1,",")
		if len(setstr1) < 1:
			return 1
		if len(dat2) < 2 :
			setstr2=["0" for x in xrange(len(setstr1))]
		else:
			setstr2=string.split(dat2,",")
		self.data.append([ph,[0],[0]])
		for item in map(None,setstr1,setstr2):
			self.data[-1][1].append(float(item[0]))
			self.data[-1][2].append(float(item[1]))
		self.data.sort()
	def write(self):
		xmlstr=[]
		xmlstr.append("<prc name=\"%s\" " % self.name)
		xmlstr[-1]+=" gsyn=\""
		for items in self.header[1:]:
			xmlstr[-1]+="%g,"%items
		xmlstr[-1]=xmlstr[-1][:-1]
		xmlstr[-1]+= "\" >"
		
		for dat in self.data:
			smt = "\t<item ph=\"%g\" prc1=\""%dat[0]
			for val in dat[1][1:]:
				smt += "%g," % val
			smt =  smt[:-1]
			smt += "\" prc2=\""
			for val in dat[2][1:]:
				smt += "%g," % val
			smt =  smt[:-1]
			smt += "\" />"
			xmlstr.append(smt)
		xmlstr.append("</prc>")
		return xmlstr
	def prn(self):
		print "PRN PRC OBJECT: ",self.name, self.header, self.data
	def getvl(self, gsyn, ph):
		if ph < 0 : ph = -math.ceil( ph ) + 1 - ph
		if ph > 1 : ph = ph - 1
		ind = [self.data[0],self.data[0]]
		for scan in self.data:
			if scan[0] < ph : ind[0] = scan
			else:
				ind[1] = scan
				break
		bd = [self.header[0],self.header[0]]
		idx = -1
		for scan in self.header:
			if scan < gsyn :
				bd[0] = scan
				idx += 1
			else:
				bd[1] = scan
				break
		
		#print "\nDB: getvl ", bd
		if bd[1] == self.header[0]:
			if bd[0] == self.header[0]:
				bd = [self.header[0], self.header[1]]
				idx = 0
			else :
				bd = [self.header[-1],self.header[-2]]
				idx = -2
		if ph == 0 :	phsh = 0
		elif ph == 1 :	phsh = 1
		else:
			phsh=(ph-ind[0][0])/(ind[1][0] - ind[0][0])
		vl1 = (
			ind[0][1][idx]  +(ind[1][1][idx]   - ind[0][1][idx])  *phsh,
			ind[0][1][idx+1]+(ind[1][1][idx+1] - ind[0][1][idx+1])*phsh
		)
		vl2 = (
			ind[0][2][idx]  +(ind[1][2][idx]   - ind[0][2][idx])  *phsh,
			ind[0][2][idx+1]+(ind[1][2][idx+1] - ind[0][2][idx+1])*phsh 
		)
		#print "DB: getvl ", bd,vl
		return (
				vl1[0]+(vl1[1]-vl1[0])*(gsyn-bd[0])/(bd[1]-bd[0]),
				vl2[0]+(vl2[1]-vl2[0])*(gsyn-bd[0])/(bd[1]-bd[0])
				)
	
