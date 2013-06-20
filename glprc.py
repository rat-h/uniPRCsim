##################################
#
# glprc.py
# Copyright (C) Louisiana State University, Health Sciences Center
# Written by 2011-2013 Ruben Tikidji-Hamburyan <rth@nisms.krinc.ru>
#                  Will Coleman 2013 wcole4@lsuhsc.edu
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
from PyQt4 import QtGui, QtCore
import importprc
import string
import sys
from xml.sax import make_parser
import icons


class odprc:
	def __init__(self):
		self.name 	= "***"
		self.id		= None
		self.gsyn	= []
		self.data	= []
		self.f2		= False


class prcviewer(QtGui.QWidget):
	def __init__(self,prc,parent=None):
		super(prcviewer, self).__init__()
		self.prc = prc
		#self.prc.data = prc.data.sort()
		self.view=[ [True for f1 in prc.data[0][1]], [True for f2 in prc.data[0][2] ] ]
		self.axescolor			= QtGui.QColor(0, 0, 0)
		self.backgroundcolor	= QtGui.QColor(255, 255, 255)
		self.margins			=[45,15,25,10] ##Left Right Botom Top
		self.font 				= QtGui.QFont('Decorative', 10)
		self.linewidth			= 2
		self.axeswidth			= 1
		self.colors = [[], []]
		r,g,b = 255,0,0
		for i in prc.data[0][1]:
			self.colors[0].append(QtGui.QColor(r, g, b))
			r -= 32
			g += 16
			if r<0	: r=255
			if g>255: g = 0
		r,g,b = 0,0,255
		for i in prc.data[0][2]:
			self.colors[1].append(QtGui.QColor(r, g, b))
			b -= 32
			g += 16
			if b<0	: b=255
			if g>255: g = 0
		self.min = prc.data[0][1][0]
		self.max = prc.data[0][1][0]
		self.vscale, self.hscale = 1.0,0.1
		self.minmax()
		
	def resizeEvent(self,event):
		#self.setFixedSize(event.size())
		size=event.size()
		self.vscale = (self.max - self.min)/(size.height() - self.margins[2] - self.margins[3])
		self.hscale = 1.0/(self.width() - self.margins[0] - self.margins[1])
		#print "Resize:%dx%d [%gx%g][%gx%g]"%(self.width(),size.height(),self.hscale,self.vscale,self.min,self.max)
		
	def paintEvent(self, event):
		#print "paint: ",
		qp  = QtGui.QPainter()
		pen = QtGui.QPen(QtCore.Qt.black, self.linewidth, QtCore.Qt.SolidLine)

		h,w = self.size().height(), self.size().width()
		#print "size: %dx%d"%(w,h),
		qp.begin(self)
		qp.setBrush(self.backgroundcolor)
		qp.drawRect(0, 0, w, h)
		idx = -1
		for i in xrange( len( self.prc.data[0][1] )):
			idx += 1
			if not self.view[0][idx]: continue
			pen.setColor( self.colors[0][idx] )
			qp.setPen(pen)
			for idd in xrange( len(self.prc.data) - 1 ):
				y0 = h - (self.prc.data[idd  ][1][i]-self.min)/self.vscale-self.margins[2]
				y1 = h - (self.prc.data[idd+1][1][i]-self.min)/self.vscale-self.margins[2]
				x0 = self.prc.data[idd  ][0] / self.hscale + self.margins[0]
				x1 = self.prc.data[idd+1][0] / self.hscale + self.margins[0]
				qp.drawLine(x0,y0,x1,y1)
		if self.prc.f2:
			idx = -1
			for i in xrange( len( self.prc.data[0][2] )):
				idx += 1
				if not self.view[1][idx]: continue
				pen.setColor( self.colors[1][idx] )
				qp.setPen(pen)
				for idd in xrange( len(self.prc.data) - 1 ):
					y0 = h - (self.prc.data[idd  ][2][i]-self.min)/self.vscale-self.margins[2]
					y1 = h - (self.prc.data[idd+1][2][i]-self.min)/self.vscale-self.margins[2]
					x0 = self.prc.data[idd  ][0] / self.hscale + self.margins[0]
					x1 = self.prc.data[idd+1][0] / self.hscale + self.margins[0]
					qp.drawLine(x0,y0,x1,y1)
		pen.setColor(self.axescolor)
		qp.setBrush(self.axescolor)
		qp.setFont(self.font)
		pen.setWidth(self.axeswidth)
		qp.setPen(pen)
		#Axes
		qp.drawLine(self.margins[0],self.margins[3],self.margins[0],h-self.margins[2])
		#Text and Tips
		qp.drawText(QtCore.QRect(0,0,self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%self.max)
		qp.drawLine(self.margins[0]-5,self.margins[3],self.margins[0],self.margins[3])
		y0 = h -(self.max/2.0 - self.min)/self.vscale-self.margins[2]
		qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%(self.max/2.0) )
		qp.drawLine(self.margins[0]-5,y0,self.margins[0],y0)
		if self.min > 0.0:
			y0 = h -self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%self.min)
			qp.drawLine(self.margins[0]-5,y0,w-self.margins[1],y0)
		elif abs(self.min) < abs(self.max)/8 :
			y0 = h + self.min/self.vscale-self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"0.0")
			qp.drawLine(self.margins[0]-5,y0,w-self.margins[1],y0)
		elif abs(self.min) < abs(self.max)/4 :
			y0 = h -self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%(self.min))
			qp.drawLine(self.margins[0]-5,y0,self.margins[0],y0)
			y0 = h + self.min/self.vscale-self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"0.0")
			qp.drawLine(self.margins[0]-5,y0,w-self.margins[1],y0)
		else :
			y0 = h -self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%(self.min))
			qp.drawLine(self.margins[0]-5,y0,self.margins[0],y0)
			y0 = h -(self.min/2.0 - self.min)/self.vscale-self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"%7.5f"%(self.min/2.0) )
			qp.drawLine(self.margins[0]-5,y0,self.margins[0],y0)
			y0 = h + self.min/self.vscale-self.margins[2]
			qp.drawText(QtCore.QRect(0,y0-self.margins[3],self.margins[0],self.margins[3]*2),QtCore.Qt.AlignCenter,"0.0")
			qp.drawLine(self.margins[0]-5,y0,w-self.margins[1],y0)
		x0 = self.margins[0] + self.prc.data[-1][0]/4.0/self.hscale
		qp.drawText(QtCore.QRect(x0-self.margins[1],y0+10,self.margins[1]*2,self.margins[3]*2),QtCore.Qt.AlignCenter,"%5.3f"%(self.prc.data[-1][0]/4.0))
		qp.drawLine(x0,y0,x0,y0+5)
		x0 = self.margins[0] + self.prc.data[-1][0]/2.0/self.hscale
		qp.drawText(QtCore.QRect(x0-self.margins[1],y0+10,self.margins[1]*2,self.margins[3]*2),QtCore.Qt.AlignCenter,"%5.3f"%(self.prc.data[-1][0]/2.0))
		qp.drawLine(x0,y0,x0,y0+5)
		x0 = self.margins[0] + self.prc.data[-1][0]*3.0/4.0/self.hscale
		qp.drawText(QtCore.QRect(x0-self.margins[1],y0+10,self.margins[1]*2,self.margins[3]*2),QtCore.Qt.AlignCenter,"%5.3f"%(self.prc.data[-1][0]*3.0/4.0))
		qp.drawLine(x0,y0,x0,y0+5)
		x0 = self.margins[0] + self.prc.data[-1][0]/self.hscale
		qp.drawText(QtCore.QRect(x0-self.margins[1],y0+10,self.margins[1]*2,self.margins[3]*2),QtCore.Qt.AlignCenter,"%5.3f"%(self.prc.data[-1][0]))
		qp.drawLine(x0,y0,x0,y0+5)
		qp.end()
		#print "done"
	def minmax(self):
		for data in self.prc.data:
			idx = 0
			for sem in data[1]:
				if self.min > sem and self.view[0][idx]: self.min = sem
				if self.max < sem and self.view[0][idx]: self.max = sem
				idx+=1
			idx = 0
			if not self.prc.f2: continue
			for sem in data[2]:
				if self.min > sem and self.view[1][idx]: self.min = sem
				if self.max < sem and self.view[1][idx]: self.max = sem
				idx+=1

class prcviewdlg(QtGui.QDialog):
	def __init__(self, prc, parent=None):
		super(prcviewdlg, self).__init__()
		self.setWindowTitle(prc.name + ' :: PRC Viewer')
		self.setGeometry(300, 300, 280, 270)
		self.view = prcviewer(prc, parent = self)
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.view)
		self.setLayout(vbox)

		
class prceditor(QtGui.QDialog):
	def __init__(self, parent=None):
		super(prceditor, self).__init__()
		self.setWindowTitle('PRC Editor')
		self.nameedit = QtGui.QLineEdit("Enter Prc name")
		importButton = QtGui.QPushButton(QtGui.QIcon(':/import.png'),"&Import",self)
		prevButton	 = QtGui.QPushButton(QtGui.QIcon(':/previewer.png'),"&Preview",self)
		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)
		setgButton	 = QtGui.QPushButton(QtGui.QIcon(':/gsyn.png'),"Reset Gsyn",self)
		clsblButton	 = QtGui.QPushButton(QtGui.QIcon(':/close-tbl.png'),"Close Table",self)
		insRowButton = QtGui.QPushButton(QtGui.QIcon(':/insert-row.png'),"Insert Row",self)
		insColButton = QtGui.QPushButton(QtGui.QIcon(':/insert-column.png'),"Insert Column",self)
		delrButton	 = QtGui.QPushButton(QtGui.QIcon(':/remove-row.png'),"Remove Row",self)
		sortButton   = QtGui.QPushButton(QtGui.QIcon(':/close-tbl.png'),"Resort Table",self)
		remButton	 = QtGui.QPushButton(QtGui.QIcon(':/remove-all.png'),"Remove All",self)
		
		hboxU = QtGui.QHBoxLayout()
		hboxU.addWidget(self.nameedit)
		hboxU.addWidget(importButton)
		hboxU.addWidget(prevButton)
		hboxU.addStretch(1)
		hboxU.addWidget(okButton )
		hboxU.addWidget(cancelButton )
		self.tbl = QtGui.QTableWidget()
		hboxD = QtGui.QHBoxLayout()
		hboxD.addStretch(1)
		hboxD.addWidget(setgButton)
		hboxD.addWidget(clsblButton)
		hboxD.addWidget(insRowButton)
		hboxD.addWidget(insColButton)
		hboxD.addWidget(delrButton)
		hboxD.addWidget(sortButton)
		hboxD.addWidget(remButton)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hboxU)
		vbox.addWidget(self.tbl)
		vbox.addLayout(hboxD)
		self.setLayout(vbox)

		self.prc=None
		self.importer = None
		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
		self.connect(importButton, QtCore.SIGNAL('clicked()'), self.importprc)
		self.connect(prevButton, QtCore.SIGNAL('clicked()'), self.preview)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(setgButton, QtCore.SIGNAL('clicked()'), self.setgsyn)
		self.connect(clsblButton, QtCore.SIGNAL('clicked()'), self.closetbl)
		self.connect(insRowButton, QtCore.SIGNAL('clicked()'), self.insertrow)
		self.connect(insColButton, QtCore.SIGNAL('clicked()'), self.insertcol)
		self.connect(delrButton, QtCore.SIGNAL('clicked()'), self.deleterow)
		self.connect(sortButton, QtCore.SIGNAL('clicked()'), self.resort)
		self.connect(remButton, QtCore.SIGNAL('clicked()'), self.clear)
	def setprc(self, prc):
		if self.prc != None: del self.prc
		self.prc = prc
		self.nameedit.setText(self.prc.name)
		self.readprc()
		
	def importprc(self):
		filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '',
		"Prc Xml Model(*.pxm);; Data file (*.dat *.data)")
		if len(filename) == 0: return
		if filename[-4:] == ".pxm" or filename[-4:] == ".PXM":
			self.readpxm(filename)
			return
		fdil = QtGui.QInputDialog(self)
		fdil.setLabelText("Select order of PRC function")
		fdil.setComboBoxEditable(False)
		fdil.setComboBoxItems(["first order", "second order"])
		ok = fdil.exec_()
		function = fdil.textValue()
		if not ok: return
		if self.importer == None:
			self.importer = importprc.importprc()
		if function != "first order" :
			self.importer.readfile(filename,fx="2")
		else:
			self.importer.readfile(filename)
		newprc = self.importer.getglprc()
		if newprc.gsyn == None :
			newprc.gsyn = []
			for i in xrange( len( newprc.data[0][1]) ):
				dok = False
				while not dok:
					double,ok = QtGui.QInputDialog.getText(self,"PRC Editor","Set gsyn value for column %d in imported file"%i)
					double,dok = double.toDouble()
				newprc.gsyn.append("%g"%double)
		else:
			newprc.gsyn = string.split(newprc.gsyn,',')
		if len( newprc.gsyn ) != len( newprc.data[0][1])  :
			for i in xrange( len( newprc.data[0][1]) - len( newprc.gsyn ) ):
				dok = False
				while not dok:
					double,ok = QtGui.QInputDialog.getText(self,"PRC Editor","Set gsyn value for column %d in imported file"%(i+len( newprc.gsyn )-1) )
					double,dok = double.toDouble()
				newprc.gsyn.append("%g"%double)
		elif (len( newprc.gsyn) < len( newprc.data[0][2]) ) and (newprc.f2 == True):
			for i in xrange( len( newprc.data[0][2]) -len( newprc.gsyn ) ):
				dok = False
				while not dok:
					double,ok = QtGui.QInputDialog.getText(self,"PRC Editor","Set gsyn value for column %d in imported file"%i)
					double,dok = double.toDouble()
				newprc.gsyn.append("%g"%double)
		self.importer.gsyn=string.join(newprc.gsyn,',')
		if self.prc != None:
			newprc.id=self.prc.id
			newprc.name=self.prc.name
			del self.prc
		self.prc = newprc
		self.readprc()
		
	def readpxm(self,filename):
		pparser = importprc.prcparcerpxm(mode="list")
		parser=make_parser()
		parser.setContentHandler(pparser)
		parser.parse(filename.toUtf8().data())
		fdil = QtGui.QInputDialog(self)
		fdil.setLabelText("Select exctracted PRC function")
		fdil.setComboBoxEditable(False)
		fdil.setComboBoxItems(pparser.prclst)
		ok = fdil.exec_()
		function = fdil.textValue()
		if not ok: return
		self.clear()
		if self.importer != None:
			del self.importer
		self.importer = importprc.importprc()
		self.importer.name = function
		self.importer.readfile(filename.toUtf8().data(),format="pxm")
		if self.prc != None:
			del self.prc
		self.prc = self.importer.getglprc()
		self.prc.gsyn = string.split(self.prc.gsyn,',')
		self.readprc()
		
	def readprc(self, prcobj=None):
		if prcobj != None:
			self.prc = prcobj
		self.tbl.clear()
		hitem = ["ph"]
		for gsn in self.prc.gsyn:
			hitem.append("F1:%s"%gsn)
		if self.prc.f2:
			self.tbl.setColumnCount(1 + len(self.prc.gsyn) *2 )
			for gsn in self.prc.gsyn:
				hitem.append("F2:%s"%gsn)
		else:
			self.tbl.setColumnCount(1 + len(self.prc.gsyn) )
		self.tbl.setHorizontalHeaderLabels(hitem)
		row = 0
		self.tbl.setRowCount( len(self.prc.data) )
		
		for data in self.prc.data:
			col = 0
			item = QtGui.QTableWidgetItem(data[0])
			item.setData(0,data[0])
			self.tbl.setItem(row,col,item)
			for fd in xrange(len(data[1])):
	
				col+=1				
				item = QtGui.QTableWidgetItem(data[0])
				item.setData(0,data[1][fd])
				self.tbl.setItem(row,col,item)
			for fd in xrange(len(data[2])):
				col+=1				
				item = QtGui.QTableWidgetItem(data[0])
				item.setData(0,data[2][fd])
				self.tbl.setItem(row,col,item)

			
			
				
			row += 1
		self.nameedit.setText(self.prc.name)
	def insertrow(self):
		self.prc.data.append(["0.000000",[],[] ] )
		for i in self.prc.data[0][1]:
			self.prc.data[-1][1].append("0.000000")
		for i in self.prc.data[0][2]:
			self.prc.data[-1][2].append("0.000000")
		self.readprc()
	def insertcol(self):
		fdil = QtGui.QInputDialog(self)
		fdil.setLabelText("Select order of new PRC column")
		fdil.setComboBoxEditable(False)
		fdil.setComboBoxItems(["first order", "first and second order"])
		ok = fdil.exec_()
		function = fdil.textValue()
		if not ok: return
		double,ok = QtGui.QInputDialog.getText(self,"PRC Editor","Set gsyn value for column this column" )
		if not ok: return
		if function == "first order":
			for rows in self.prc.data:
				rows[1].append("x.x")
		else:
			self.prc.f2 = True
			for rows in self.prc.data:
				rows[1].append("x.x")
				rows[2].append("x.x")
		self.prc.gsyn.append(float(double))
		self.readprc()
	def closetbl(self):
		if len(self.prc.data[0][1]) != len(self.prc.data[0][2]): return
		self.insertrow()
		self.prc.data[-1][0]="1.000000"
		for idx in xrange(len( self.prc.data[0][1] ) ):
			self.prc.data[-1][2][idx] = self.prc.data[0][1][idx]
			self.prc.data[-1][1][idx] = "0.000000"
		self.readprc()
		
	def clear(self):
		if 	self.prc != None:
			del self.prc
			self.prc = None
		if self.importer != None:
			del self.importer
			self.importer = None
		self.tbl.clear()
		self.tbl.setRowCount(0)
		self.tbl.setColumnCount(0)
	def preview(self):
		if self.prc == None: return
		if not self.upDate(): return
		dprc = odprc()
		dprc.name = self.prc.name
		dprc.gsyn = [ float(syn) for syn in self.prc.gsyn]
		dprc.f2 = self.prc.f2
		for data in self.prc.data:
			dprc.data.append([ float(data[0]), [float(d1) for d1 in data[1] ], [float(d2) for d2 in data[2] ] ])
		prcview = prcviewdlg(dprc,self)
		prcview.exec_()
	def resort(self):
		self.tbl.sortByColumn(0,QtCore.Qt.AscendingOrder)
	def rename(self):
		if self.prc == None:
			self.prc = odprc()
		self.prc.name = self.nameedit.text()
		self.setWindowTitle(self.prc.name+' :: PRC Editor')
	def setgsyn(self):
		if self.prc == None: return
		for ind in xrange(len(self.prc.gsyn)):
			double,ok = QtGui.QInputDialog.getText(self,"PRC Editor","Set gsyn value for column %d [%g]"%(ind,self.prc.gsyn[ind]) )
			if ok:
				self.prc.gsyn[ind]=(float(double))
		hitem = ["ph"]
		for gsn in self.prc.gsyn:
			hitem.append("F1:%g"%gsn)
		if self.prc.f2:
			self.tbl.setColumnCount(1 + len(self.prc.gsyn) *2 )
			for gsn in self.prc.gsyn:
				hitem.append("F2:%g"%gsn)
		else:
			self.tbl.setColumnCount(1 + len(self.prc.gsyn) )
		self.tbl.setHorizontalHeaderLabels(hitem)
	def deleterow(self):
		didx = self.tbl.currentRow()
		
		if didx < 0 : return
		self.prc.data = self.prc.data[0:didx]+self.prc.data[didx+1:]
		self.readprc()
	def upDate(self):
		if self.nameedit.text().length() < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the name of PRC ",QtGui.QMessageBox.Ok,0)
			return False
		####Test!
		fl = len(self.prc.data[0][1])
		for idx in xrange(self.tbl.rowCount()):
			if fl < len(self.prc.data[idx][1]): fl = len(self.prc.data[idx][1])
			if fl < len(self.prc.data[idx][2]): fl = len(self.prc.data[idx][2])
		flg = False
		for idx in xrange(self.tbl.rowCount()):
			if fl > len(self.prc.data[idx][1]):
				self.prc.data[idx][1] += [ "xx" for cnt in xrange(fl - len(self.prc.data[idx][1]) ) ]
				flg = True
			if fl > len(self.prc.data[idx][2]) and len(self.prc.data[0][2]) != 0:
				self.prc.data[idx][2] += [ "xx" for cnt in xrange(fl - len(self.prc.data[idx][2]) ) ]
				flg = True
		if flg: self.readprc()
		for idx in xrange(self.tbl.rowCount()):
			idd = 0
			data,ok = self.tbl.item(idx,0).data(0).toDouble()
			if not ok:
				QtGui.QMessageBox.critical(self,"Critical ERROR!","The cell %dx%d isn't an number!"%(idx,idd),QtGui.QMessageBox.Ok,0)
				return False
			self.prc.data[idx][0] = "%12.9f"%data
			for iter in xrange( len(self.prc.data[idx][1]) ):
				idd += 1
				data,ok = self.tbl.item(idx,idd).data(0).toDouble()
				if not ok:
					QtGui.QMessageBox.critical(self,"Critical ERROR!","The cell %dx%d isn't an number!"%(idx,idd),QtGui.QMessageBox.Ok,0)
					return False
				self.prc.data[idx][1][iter] = "%g"%data
			if not self.prc.f2: continue
			for iter in xrange( len(self.prc.data[idx][2]) ):
				idd += 1
				data,ok = self.tbl.item(idx,idd).data(0).toDouble()
				if not ok:
					QtGui.QMessageBox.critical(self,"Critical ERROR!","The cell %dx%d isn't an number!"%(idx,idd),QtGui.QMessageBox.Ok,0)
					return False
				self.prc.data[idx][2][iter] = "%g"%data
		self.prc.name=self.nameedit.text().toUtf8().data()
		self.readprc()
		return True
			
			
	def ok(self):
		if not self.upDate(): return

		#Will
		# Check that ph ends with one. If last ph is less than one, prompt user to decide how to add row with ph = 1.
		
		lastRow = len(self.prc.data)-1
		order = 0
		for iter in xrange(1, len(self.prc.data[0])):
			if self.prc.data[0][iter] : # Check for empty lists
				order+=1		
		if float(str(self.prc.data[0][0])) > 0: # first ph value is greater than zero
			checkZeroOrderOneDialogOptions = ["Set resetting at ph = 0.0 to zero", "Set resetting at ph = 0.0 by extrapolation", "Enter decimal value(s) of resetting at ph = 0.0"]
			#Use fewer options when no value at ph = 1 is found
			checkZeroOrderTwoDialogFewerOptions = ["Set both order resettings at ph = 0.0 to zero", "Set both order resettings at ph = 1.0 by extrapolation", "Enter decimal value(s) of resetting at ph = 0.0"]
			checkZeroOrderTwoDialogOptions = ["Set both order resettings at ph = 0.0 to zero", "Set both order resettings at ph = 1.0 by extrapolation", "Set first order resetting at ph = 0.0 to value of second order at ph = 1.0 and vice versa", "Set first order resetting at ph = 0.0 to zero and second order resetting at ph = 0 to value of first order resetting at ph = 1.0", "Enter decimal value(s) of resetting at ph = 0.0"]
			phGreaterThanZeroDialog = QtGui.QInputDialog(self)
			phGreaterThanZeroDialog.setComboBoxEditable(False)
			labelTextGreaterThanZero = "The first value for the phase (ph) is greater than 0. It must be 0 in order for the uniPRCsim to work correctly.\nProvided are some options for fixing this value.\n\nWhat would you like to do?"
			if(order==1):
				#print("order is one, doesn't matter if ph at 1 exists")
				phGreaterThanZeroDialog.setLabelText(labelTextGreaterThanZero)
				phGreaterThanZeroDialog.setComboBoxItems(checkZeroOrderOneDialogOptions)
			else:
				if float(str(self.prc.data[lastRow][0])) < 1:#Use fewer options when no value at ph = 1 is found
					#print("order 2, ph value of 1 doesn't exist either, offer fewer options")
					phGreaterThanZeroDialog.setLabelText(labelTextGreaterThanZero)
					phGreaterThanZeroDialog.setComboBoxItems(checkZeroOrderTwoDialogFewerOptions)
					
				else:
					#print("order 2, ph value of 1 exists and value of zero does not, offer all options")
					phGreaterThanZeroDialog.setLabelText(labelTextGreaterThanZero)
					phGreaterThanZeroDialog.setComboBoxItems(checkZeroOrderTwoDialogOptions)
			ok = phGreaterThanZeroDialog.exec_()
			if ok == 0: return

			returned = phGreaterThanZeroDialog.textValue()
			prcList = list()
			prcList2 = list()
			numberOfGsyns = 0
			if returned == str(checkZeroOrderOneDialogOptions[0]) or returned == str(checkZeroOrderTwoDialogFewerOptions[0]) or returned == str(checkZeroOrderTwoDialogOptions):
				while(numberOfGsyns < len(self.prc.gsyn)):
					prcList.append("0.000000")
					numberOfGsyns +=1
					
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						prcList2.append("0.000000")
						numberOfGsyns +=1
			
			if returned == str(checkZeroOrderOneDialogOptions[1]) or returned == str(checkZeroOrderTwoDialogFewerOptions[1]) or returned == str(checkZeroOrderTwoDialogOptions[1]): 
				while(numberOfGsyns < len(self.prc.gsyn)):
					
					firstValuePRC = float(self.prc.data[0][1][numberOfGsyns])
					firstValuePH = float(self.prc.data[0][0])
					secondValuePRC = float(self.prc.data[1][1][numberOfGsyns])
					secondValuePH = float(self.prc.data[1][0])
					differenceBetweenZeroAndFirstPH = firstValuePH
					slope = (secondValuePRC - firstValuePRC)/(secondValuePH - firstValuePH)
					extrapolatedValue = -(slope * differenceBetweenZeroAndFirstPH) + firstValuePRC
					prcList.append(str(extrapolatedValue))
					numberOfGsyns +=1
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						firstValuePRC = float(self.prc.data[0][2][numberOfGsyns])
						firstValuePH = float(self.prc.data[0][0])
						secondValuePRC = float(self.prc.data[1][2][numberOfGsyns])
						secondValuePH = float(self.prc.data[1][0])
						differenceBetweenZeroAndFirstPH = firstValuePH
						slope = (secondValuePRC - firstValuePRC)/(secondValuePH - firstValuePH)
						extrapolatedValue = -(slope * differenceBetweenZeroAndFirstPH) + firstValuePRC
						prcList2.append(str(extrapolatedValue))
						numberOfGsyns +=1
			
			if returned == str(checkZeroOrderOneDialogOptions[2]) or returned == str(checkZeroOrderTwoDialogFewerOptions[2]) or returned == str(checkZeroOrderTwoDialogOptions[4]):
				while(numberOfGsyns < len(self.prc.gsyn)):
					floatEntered = False
					while(floatEntered == False):
						userEnterValueDialog = QtGui.QInputDialog(self)
						userEnterValueDialog.setLabelText("Enter a value for prc(s)")
						userEnterValueDialog.setComboBoxEditable(True)
						ok = userEnterValueDialog.exec_()
						if ok == 0: return
					
						try:
							userEnteredValue = float(userEnterValueDialog.textValue())
							floatEntered = True
							prcList.append(str(userEnteredValue))
							
						except ValueError:
							notFloatValueMessage = QtGui.QMessageBox(self)
							notFloatValueMessage.setText("You must enter a float value.")
							notFloatValueMessage.exec_()
					numberOfGsyns +=1
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						floatEntered = False
						while(floatEntered == False):
							userEnterValueDialog = QtGui.QInputDialog(self)
							userEnterValueDialog.setLabelText("Enter a value for prc(s)")
							userEnterValueDialog.setComboBoxEditable(True)
							ok = userEnterValueDialog.exec_()
							if ok == 0: return
						
							try:
								userEnteredValue = float(userEnterValueDialog.textValue())
								floatEntered = True
								prcList2.append(str(userEnteredValue))
								
							except ValueError:
								notFloatValueMessage = QtGui.QMessageBox(self)
								notFloatValueMessage.setText("You must enter a float value.")
								notFloatValueMessage.exec_()
						numberOfGsyns +=1
			if returned == str(checkZeroOrderTwoDialogOptions[2]):
				#Set first order resetting at ph = 0.0 to value of second order at ph = 1.0 and vice versa
				prcList = self.prc.data[lastRow][2][:]
				prcList2 = self.prc.data[lastRow][1][:]
				
			if returned == str(checkZeroOrderTwoDialogOptions[3]):
				#Set first order resetting at ph = 0.0 to zero and second order resetting at ph = 0 to value of first order resetting at ph = 1.0
				prcList2 = self.prc.data[lastRow][1][:]
				while(numberOfGsyns < len(self.prc.gsyn)):
					prcList.append("0.000000")
					numberOfGsyns +=1
					
			self.prc.data.insert(0,["0.000000",prcList,prcList2 ])
		
		
		
		
		#Second set of checks for ph value less than one	
		lastRow = len(self.prc.data)-1
		if float(str(self.prc.data[lastRow][0])) < 1: #last ph value is less than one
			checkOneOrderOneDialogOptions = ["Set resetting at ph = 1.0 to zero", "Set resetting at ph = 1.0 to value of resetting at ph = 0", "Set resetting at ph = 1.0 by extrapolation", "Enter decimal value(s) of resetting at ph = 1.0"]
			checkOneOrderTwoDialogOptions = ["Set first and second order resettings at ph = 1.0 to zero", "Set resetting at ph = 1.0 to value of first order resetting at ph = 0", "Set both order resettings at ph = 1.0 by extrapolation", "Set first order resetting at ph = 1.0 to value of second order at ph = 0.0 and vice versa","Set first order resetting at ph = 1.0 to value of second order at ph = 0.0 and second order resetting at ph = 1 to zero","Enter decimal value(s) of resetting at ph = 1.0"]
			phLessThanOneDialog = QtGui.QInputDialog(self)
			phLessThanOneDialog.setComboBoxEditable(False)
			labelTextLessThanOne = "The last value for the phase (ph) is less than 1. It must be 1 in order for the uniPRCsim to work correctly.\nProvided are some options for fixing this value.\n\nWhat would you like to do?"
			if(order==1):#Fewer options
				phLessThanOneDialog.setLabelText(labelTextLessThanOne)
				phLessThanOneDialog.setComboBoxItems(checkOneOrderOneDialogOptions)
			else :# when second order prc
				phLessThanOneDialog.setLabelText(labelTextLessThanOne)
				phLessThanOneDialog.setComboBoxItems(checkOneOrderTwoDialogOptions)

			ok = phLessThanOneDialog.exec_()
			if ok == 0: return

			returned = phLessThanOneDialog.textValue()
			
			prcList = list()
			prcList2 = list()
			numberOfGsyns = 0
			if returned == str(checkOneOrderOneDialogOptions[0]) or returned == str(checkOneOrderTwoDialogOptions[0]):
				
				while(numberOfGsyns < len(self.prc.gsyn)):
					prcList.append("0.000000")
					numberOfGsyns +=1
					
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						prcList2.append("0.000000")
						numberOfGsyns +=1
			
			if returned == str(checkOneOrderOneDialogOptions[1]):
				prcList = self.prc.data[0][1][:]

			if returned == str(checkOneOrderTwoDialogOptions[1]):
				prcList = self.prc.data[0][1][:]
				prcList2 = self.prc.data[0][1][:]
				
			if returned == str(checkOneOrderOneDialogOptions[2]) or returned == str(checkOneOrderTwoDialogOptions[2]):
				while(numberOfGsyns < len(self.prc.gsyn)):
					
					firstValuePRC = float(self.prc.data[lastRow-1][1][numberOfGsyns])
					firstValuePH = float(self.prc.data[lastRow-1][0])
					secondValuePRC = float(self.prc.data[lastRow][1][numberOfGsyns])
					secondValuePH = float(self.prc.data[lastRow][0])
					differenceBetweenOneAndLastPH = 1-secondValuePH
					slope = (secondValuePRC - firstValuePRC)/(secondValuePH - firstValuePH)
					extrapolatedValue = (slope * differenceBetweenOneAndLastPH) + secondValuePRC
					prcList.append(str(extrapolatedValue))
					numberOfGsyns +=1
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						firstValuePRC = float(self.prc.data[lastRow-1][2][numberOfGsyns])
						firstValuePH = float(self.prc.data[lastRow-1][0])
						secondValuePRC = float(self.prc.data[lastRow][2][numberOfGsyns])
						secondValuePH = float(self.prc.data[lastRow][0])
						differenceBetweenOneAndLastPH = 1-secondValuePH
						slope = (secondValuePRC - firstValuePRC)/(secondValuePH - firstValuePH)
						extrapolatedValue = (slope * differenceBetweenOneAndLastPH) + secondValuePRC
						prcList2.append(str(extrapolatedValue))
						numberOfGsyns +=1
						
			if returned == str(checkOneOrderTwoDialogOptions[3]):
				prcList = self.prc.data[0][2][:]
				prcList2 = self.prc.data[0][1][:]
			
			if returned == str(checkOneOrderTwoDialogOptions[4]):
				prcList = self.prc.data[0][2][:]
				while(numberOfGsyns < len(self.prc.gsyn)):
					prcList2.append("0.000000")
					numberOfGsyns +=1
				
			if returned == str(checkOneOrderOneDialogOptions[3]) or returned == str(checkOneOrderTwoDialogOptions[5]):
				while(numberOfGsyns < len(self.prc.gsyn)):
					floatEntered = False
					while(floatEntered == False):
						userEnterValueDialog = QtGui.QInputDialog(self)
						userEnterValueDialog.setLabelText("Enter a value for prc(s)")
						userEnterValueDialog.setComboBoxEditable(True)
						ok = userEnterValueDialog.exec_()
						if ok == 0: return
					
						try:
							userEnteredValue = float(userEnterValueDialog.textValue())
							floatEntered = True
							prcList.append(str(userEnteredValue))
							
						except ValueError:
							notFloatValueMessage = QtGui.QMessageBox(self)
							notFloatValueMessage.setText("You must enter a float value.")
							notFloatValueMessage.exec_()
					numberOfGsyns +=1
				if(order==2):
					numberOfGsyns = 0
					while(numberOfGsyns < len(self.prc.gsyn)):
						floatEntered = False
						while(floatEntered == False):
							userEnterValueDialog = QtGui.QInputDialog(self)
							userEnterValueDialog.setLabelText("Enter a value for prc(s)")
							userEnterValueDialog.setComboBoxEditable(True)
							ok = userEnterValueDialog.exec_()
							if ok == 0: return
						
							try:
								userEnteredValue = float(userEnterValueDialog.textValue())
								floatEntered = True
								prcList2.append(str(userEnteredValue))
								
							except ValueError:
								notFloatValueMessage = QtGui.QMessageBox(self)
								notFloatValueMessage.setText("You must enter a float value.")
								notFloatValueMessage.exec_()
						numberOfGsyns +=1
						
			self.prc.data.append(["1.000000",prcList,prcList2 ])

		if(self.prc.name=="..."):
			userEnterPRCNameDialog = QtGui.QInputDialog(self)
			userEnterPRCNameDialog.setLabelText("Enter a name for PRC")
			userEnterPRCNameDialog.setComboBoxEditable(True)
			ok = userEnterPRCNameDialog.exec_()
			if ok == 0: return
			self.prc.name = userEnterPRCNameDialog.textValue()
		
		#End Will
		self.accept()
	def cancel(self):
		#do something to save
		self.reject()
			
		

		
class glprc:
	
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "prc"
		prcinsr = QtGui.QAction(QtGui.QIcon(':/prc.png'), 'Insert/Edit PRC', mainwnd)
		prcinsr.setShortcut('Ctrl+P')
		prcinsr.setStatusTip('Insert or Edit selected PRC')
		mainwnd.connect(prcinsr, QtCore.SIGNAL('triggered()'), self.insert)
		prcprvw = QtGui.QAction(QtGui.QIcon(':/previewer.png'), 'Preview PRC', mainwnd)
		prcprvw.setShortcut('Alt+P')
		prcprvw.setStatusTip('Preview PRC')
		mainwnd.connect(prcprvw, QtCore.SIGNAL('triggered()'), self.preview)
		prcmenu = menubar.addMenu('&PRC')
		prcmenu.addAction(prcinsr)
		prcmenu.addAction(prcprvw)
		toolbar.addAction(prcinsr)
		toolbar.addAction(prcprvw)
		self.prclst		= []
		self.ischanged	= False
		self.tmpprc = None
	def clean(self):
		del self.prclst
		self.prclst = []
		self.ischanged	= False
		self.tmpprc = None
		
	def insert(self):
		if not self.parent.isactive : return
		edit=prceditor(parent=self.mainwnd)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes PRC item((("
			else:
				edit.readprc(prcobj=self.prclst[prcid])
		if not edit.exec_(): return
		self.ischanged	= True
		if ok :
			self.prclst[prcid] = edit.prc
			item.setText(2,edit.prc.name)
		else:
			newprc = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newprc)
			newprc.setIcon(0,QtGui.QIcon(':/prc.png'))
			newprc.setText(1,'PRC:')
			newprc.setText(2,edit.prc.name)
			newprc.setData(1,QtCore.Qt.UserRole,self.object)
			newprc.setData(2,QtCore.Qt.UserRole,len(self.prclst))
			edit.prc.id = newprc
			self.prclst.append(edit.prc)
		
	def preview(self):
		if not self.parent.isactive : return
		if self.prclst == None: return
		item = self.mainwnd.tree.currentItem()
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		prc=self.prclst[prcid]
		dprc = odprc()
		dprc.name = prc.name
		dprc.gsyn = [ float(syn) for syn in prc.gsyn]
		dprc.f2 = prc.f2
		for data in prc.data:
			dprc.data.append([ float(data[0]), [float(d1) for d1 in data[1] ], [float(d2) for d2 in data[2] ] ])
		prcview = prcviewdlg(dprc,self)
		prcview.exec_()
	def remove(self, item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		prcid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.prclst) <= prcid : return
		del self.prclst[prcid].data
		self.prclst[prcid].id = None
		self.ischanged	= True
	def click(self):
		self.preview()	
	def save(self):
		result = []
		for prc in self.prclst:
			if prc.id == None: continue
			result.append("<prc name=\"%s\" gsyn=\"%s\">"%(prc.name,string.join(prc.gsyn,",")) )
			for item in prc.data:
				if prc.f2 :
					result.append("\t<item ph=\"%s\" prc1=\"%s\" prc2=\"%s\" />"%(item[0],string.join(item[1],","),string.join(item[2],",")) )
				else:
					result.append("\t<item ph=\"%s\" prc1=\"%s\" />"%(item[0],string.join(item[1],",")) )
			result.append("</prc>")
		self.ischanged	= False
		return result
	def startpoint(self,name,attr={}):
		if name == "prc" and self.tmpprc == None and attr.get("name",0) and attr.get("gsyn",0):
			self.tmpprc = odprc()
			self.tmpprc.name = attr["name"]
			self.tmpprc.gsyn = string.split(attr["gsyn"],",")
			return
		elif name == "item" and self.tmpprc != None and attr.get("ph",0) and attr.get("prc1",0):
			self.tmpprc.data.append([ attr["ph"],string.split(attr["prc1"],","),[] ])
			if attr.get("prc2",0):
				self.tmpprc.data[-1][2] = string.split(attr["prc2"],",")
				self.tmpprc.f2 = True
			return
		
		QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag <%s>!"%name,QtGui.QMessageBox.Ok,0)
		return
	def stoppoint(self,name):
		if name == "item" and self.tmpprc != None: return
		elif name == "prc" and self.tmpprc != None:
			newprc = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newprc)
			newprc.setIcon(0,QtGui.QIcon(':/prc.png'))
			newprc.setText(1,'PRC:')
			newprc.setText(2,self.tmpprc.name)
			newprc.setData(1,QtCore.Qt.UserRole,self.object)
			newprc.setData(2,QtCore.Qt.UserRole,len(self.prclst))
			self.tmpprc.id = newprc
			self.prclst.append(self.tmpprc)
			self.tmpprc = None
			return
		QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag closing <%s>!"%name,QtGui.QMessageBox.Ok,0)
		return
		
	def getnames(self):
		result = []
		for x in self.prclst:
			if x.id == None: continue
			result.append(x.name)
		return result
	def getdata(self,name):
		for x in self.prclst:
			if x.id == None: continue
			if x.name != name : continue
			return x
		

if __name__ == '__main__':
	prc = odprc()
	prc.name = "name"
	prc.gsyn=[0.5]
	for x in xrange(11):
		prc.data.append([ float(x)/10.0,[float(x*x)],[] ])
	
	app = QtGui.QApplication(sys.argv)
	ex = prceditor()
	ex.show()
	#ex=prcviewdlg(prc)
	#ex.exec_()
	app.exec_()
