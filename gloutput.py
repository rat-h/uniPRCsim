import sys
from PyQt4 import QtGui, QtCore

import csv
import icons


class odrastr:
	def __init__(self,filename):
		
		fd = open(filename,"r")
		self.data = []
		self.header = None
		data = csv.reader(fd)
		for row in data:
			if len(row) < 2: continue
			if self.header == None:
				self.header = row
			else:
				self.data.append([ float(x) for x in row[0:2] ]+ [int(x) for x in row[2:] ] )
		#print self.header
		#print self.data[0]
			
class rastrwd(QtGui.QWidget):
	def __init__(self,parent=None):
		super(rastrwd, self).__init__(parent)
		self.parent				=parent
		self.view				= []
		self.axescolor			= QtGui.QColor(0, 0, 0)
		self.backgroundcolor	= QtGui.QColor(255, 255, 255)
		self.margins			= [45,20,25,10] ##Left Right Botom Top
		self.font 				= QtGui.QFont('Decorative', 10)
		self.linewidth			= 2
		self.axeswidth			= 1
		self.channels			= 0
		self.data				= None
		self.t_left				= 0.0
		self.t_right			= 0.0
		self.vscale				= 0.0
		self.hscale				= 0.0
		self.d_left_idx			= 0
		self.d_len				= 500
		self.image				= None
		self.collors			= []
		
	def resizeEvent(self,event):
		super(rastrwd, self).resizeEvent(event)
		if self.data == None: return
		size=event.size()
		self.vscale = float(size.height() - self.margins[2] - self.margins[3])/self.channels
		self.hscale = (self.t_right - self.t_left)/(self.width() - self.margins[0] - self.margins[1])
		if self.image != None: del self.image
	def paintEvent(self, event):
		super(rastrwd, self).paintEvent(event)
		if self.data == None:return
		qp  = QtGui.QPainter()
		pen = QtGui.QPen(QtCore.Qt.black, self.linewidth, QtCore.Qt.SolidLine)
		h,w = self.size().height(), self.size().width()
		qp.begin(self)
		qp.setBrush(self.backgroundcolor)
		qp.drawRect(0, 0, w, h)
		for cnt in xrange (self.d_len):
			x0 = self.margins[0] + (self.data.data[cnt+self.d_left_idx][0] - self.t_left)/self.hscale
			chv = -1
			for ch in xrange(self.channels):
				if not self.view[ch]: continue
				chv += 1
				if self.data.data[cnt+self.d_left_idx][ch+2] :
					y0 = h - float(chv)*self.vscale-self.margins[2]
					y1 = h - float(chv+1)*self.vscale-self.margins[2]
					if  (y0 - y1) > 10:
						y0 -= 3
						y1 += 3
					elif (y0 - y1) > 4:
						y0 -= 1
						y1 += 1
					pen.setColor(self.collors[ch])
					qp.setPen(pen)
					qp.drawLine(x0,y0,x0,y1)
		pen.setColor(self.axescolor)
		qp.setPen(pen)
		chv = -1
		for ch in xrange(self.channels):
			if not self.view[ch]: continue
			chv += 1
			y0 = h - float(chv)*self.vscale-self.margins[2]
			y1 = h - float(chv+1)*self.vscale-self.margins[2]
			qp.drawText(QtCore.QRect(0,y1,self.margins[0],(y0-y1)),QtCore.Qt.AlignCenter,self.data.header[ch+2])
		x0 = self.margins[0] + (self.data.data[self.d_left_idx][0] - self.t_left)/self.hscale
		x1 = self.margins[0] + (self.data.data[self.d_len + self.d_left_idx][0] - self.t_left)/self.hscale
		qp.drawLine(x0,h - self.margins[2],x1, h - self.margins[2])
		qp.drawLine(x0,h - self.margins[2],x0,h - self.margins[2]+self.margins[3]/2)
		qp.drawText(QtCore.QRect(x0-self.margins[1],h-self.margins[3],self.margins[1]*2,self.margins[3]),QtCore.Qt.AlignCenter,"%g"%self.data.data[self.d_left_idx][0])
		qp.drawLine(x1,h - self.margins[2],x1,h - self.margins[2]+self.margins[3]/2)
		qp.drawText(QtCore.QRect(x1-self.margins[1],h-self.margins[3],self.margins[1]*2,self.margins[3]),QtCore.Qt.AlignCenter,"%g"%self.data.data[self.d_len + self.d_left_idx][0])
		dind = (self.d_len/2 +  self.d_left_idx)
		x0 = self.margins[0] + (self.data.data[dind][0] - self.t_left)/self.hscale
		qp.drawLine(x0,h - self.margins[2],x0,h - self.margins[2]+self.margins[3]/2)
		qp.drawText(QtCore.QRect(x0-self.margins[1],h-self.margins[3],self.margins[1]*2,self.margins[3]),QtCore.Qt.AlignCenter,"%g"%self.data.data[dind][0])
		
		qp.end()
	def readfile(self, filename):
		self.data = odrastr(filename)
		if len(self.data.data) < 500:
			self.d_len = len(self.data.data) - 2
		else:
			self.d_len				= 500#len(self.data.data) -1
		self.t_left				= 0.0
		self.t_right			= self.data.data[self.d_len][0]#self.data.data[-1][0]
		self.d_left_idx			= 0
		
		self.channels			= len(self.data.data[-1]) - 2
		self.collors			= []
		r,g,b	= 255,0,0
		for x in xrange(self.channels):
			r -= 15
			g += 7
			b += 3
			if r <= 0: r = 255
			if g >= 256 : g = 0
			if b >= 256: b = 0
			self.collors.append( QtGui.QColor(r, g, b) )
		self.view				= [ True for x in xrange(self.channels) ]
		self.rescale()

	def rescale(self):
		h,w = self.size().height(), self.size().width()
		self.t_right			= self.data.data[self.d_len+self.d_left_idx][0]
		self.t_left				= self.data.data[self.d_left_idx][0]
		self.vscale = float(h - self.margins[2] - self.margins[3])/self.channels
		self.hscale = (self.t_right - self.t_left)/(w - self.margins[0] - self.margins[1])
		self.parent.scroller.setMaximum(len(self.data.data)-self.d_len-2)
		self.parent.scroller.setPageStep(self.d_len)
		self.update()

	def scroll(self, item):
		self.t_left				= self.data.data[item][0]
		self.t_right			= self.data.data[item+self.d_len][0]
		self.d_left_idx			= item
		h,w = self.size().height(), self.size().width()
		self.vscale = float(h - self.margins[2] - self.margins[3])/self.channels
		self.hscale = (self.t_right - self.t_left)/(w - self.margins[0] - self.margins[1])
		self.update()
	def zoomin(self):
		self.d_len = int(self.d_len * 0.75)
		if self.d_len < 4: self.d_len = 4
		self.rescale()
	def zoomout(self):
		self.d_len = int(self.d_len * 1.25)
		if (self.d_len + self.d_left_idx) >= len(self.data.data):
			if self.d_len < len(self.data.data):
				self.d_left_idx = len(self.data.data) - self.d_len-1
			else:
				self.d_left_idx = 0
				self.d_len = len(self.data.data)
			self.parent.scroller.setValue(self.d_left_idx)		
		self.rescale()
	def getsvg(self):
		if self.data == None:return
		filename = QtGui.QFileDialog.getSaveFileName(self.parent, 'Export to file', '', "Scalable Vector Graphics(*.svg)")
		if filename.length() < 1: return
		fd = open(filename.toUtf8().data(),"w")
		fd.write('<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>\n')
		fd.write('<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" >\n')
		fd.write('<g>\n')
		nchannels = reduce (lambda x,y: x+y, self.view)
		w,h = 1200.0, 1024
		margins = self.margins
		hscale = (self.data.data[self.d_left_idx+ self.d_len][0] - self.data.data[self.d_left_idx][0])/(w - margins[0] - margins[1])
		t_left = self.data.data[self.d_left_idx][0]
		vscale = (h -margins[2] - margins[3])/(nchannels+1)
		chv = -1
		for ch in xrange(self.channels):
			if not self.view[ch]: continue
			chv += 1
			y0 = h - float(chv)  *vscale-margins[2]
			y1 = h - float(chv+1)*vscale-margins[2]
			if  (y0 - y1) > 10:
				y0 -= 3
				y1 += 3
			elif (y0 - y1) > 4:
				y0 -= 1
				y1 += 1
			fd.write('<g>\n<text x="%g" y="%g" font-family="Verdana" font-size="16" fill="black" >%s</text>\n'%(0,(y0+y1)/2,self.data.header[ch+2] ))
			for cnt in xrange (self.d_len):
				if self.data.data[cnt+self.d_left_idx][ch+2] :
					x0 = margins[0] + (self.data.data[cnt+self.d_left_idx][0] - t_left)/hscale
					fd.write("<line style=\"stroke:black;stroke-width:2\" x1=\"%g\" y1=\"%g\" x2=\"%g\" y2=\"%g\"/>\n"%(x0,y0,x0,y1) )
			fd.write("</g>\n")
		fd.write("<g>\n")
		x0 = margins[0] + (self.data.data[self.d_left_idx][0] - self.t_left)/hscale
		x1 = margins[0] + (self.data.data[self.d_len + self.d_left_idx][0] - t_left)/hscale
		fd.write("<line style=\"stroke:black;stroke-width:3;stroke-linecap:round\" x1=\"%g\" y1=\"%g\" x2=\"%g\" y2=\"%g\"/>\n"%(x0,h - margins[2],x1, h - margins[2]) )
		fd.write("<line style=\"stroke:black;stroke-width:3;stroke-linecap:round\" x1=\"%g\" y1=\"%g\" x2=\"%g\" y2=\"%g\"/>\n"%(x0,h - margins[2],x0,h - margins[2]+ margins[3]/2) )
		fd.write('<text x="%g" y="%g" font-family="Verdana" font-size="16" fill="black" >%0.3f</text>\n'%(x0-margins[1],h-margins[3]/2,float(self.data.data[self.d_left_idx][0]) ))
		fd.write("<line style=\"stroke:black;stroke-width:3;stroke-linecap:round\" x1=\"%g\" y1=\"%g\" x2=\"%g\" y2=\"%g\"/>\n"%(x1,h - margins[2],x1,h - margins[2]+margins[3]/2) )
		fd.write('<text x="%g" y="%g" font-family="Verdana" font-size="16" fill="black" >%0.3f</text>\n'%(x1-margins[1],h-margins[3]/2,float(self.data.data[self.d_len + self.d_left_idx][0]) ))
		dind = (self.d_len/2 +  self.d_left_idx)
		x0 = margins[0] + (self.data.data[dind][0] - t_left)/hscale
		fd.write("<line style=\"stroke:black;stroke-width:2;stroke-linecap:round\" x1=\"%g\" y1=\"%g\" x2=\"%g\" y2=\"%g\"/>\n"%(x0,h - margins[2],x0,h - margins[2]+margins[3]/2) )
		fd.write('<text x="%g" y="%g" font-family="Verdana" font-size="16" fill="black" >%0.3f</text>\n'%(x0-margins[1],h-margins[3]/2,float(self.data.data[dind][0]) ))
		fd.write("</g>\n</g>\n</svg>")
		fd.close()
	def setx(self):
		print "in"
		ret = QtGui.QInputDialog.getDouble(self, "Setup Time for Left border","Left position",self.data.data[self.d_left_idx][0], self.data.data[0][0], self.data.data[-1][0])
		if not ret[1] : return
		scan,maxscan = 0,len(self.data.data)
		while self.data.data[scan][0]<ret[0] and scan < maxscan: scan += 1
		self.d_left_idx = scan
		ret = QtGui.QInputDialog.getDouble(self, "Setup Time for Left border","Left position",self.data.data[self.d_left_idx+self.d_len][0], self.data.data[0][0], self.data.data[-1][0])
		if not ret[1] : return
		while self.data.data[scan][0]<ret[0] and scan < maxscan: scan += 1
		self.d_len = scan - self.d_left_idx
		self.parent.scroller.setSliderPosition(self.d_left_idx)
		self.rescale()


class glraster(QtGui.QDialog):
	def __init__(self, parent=None):
		super(glraster, self).__init__()
		self.setWindowTitle('Rastrview')
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.resize(screen.width()*3/4, screen.height()/2)
		
		self.mainwd	= rastrwd(self)
		self.scroller = QtGui.QScrollBar(QtCore.Qt.Horizontal,self)
		zoonin	= QtGui.QPushButton(QtGui.QIcon(':/zoomin.png'),"Zoom &In",self)
		zoonout	= QtGui.QPushButton(QtGui.QIcon(':/zoomout.png'),"Zoom &Out",self)
		getsvg = QtGui.QPushButton(QtGui.QIcon(':/get-svg.png'),"",self)
		setx = QtGui.QPushButton(QtGui.QIcon(':/setup-time.png'),"",self)
		close	= QtGui.QPushButton(QtGui.QIcon(':/exit.png'),"&Close",self)
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(zoonin)
		hbox.addWidget(zoonout)
		hbox.addWidget(getsvg)
		hbox.addWidget(setx)
		#hbox.addSeparator()
		hbox.addStretch(1)
		hbox.addWidget(close)
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addWidget(self.mainwd)
		vbox.addWidget(self.scroller)
		self.setLayout(vbox)
		self.connect(self.scroller, QtCore.SIGNAL('valueChanged (int)'), self.mainwd.scroll)
		self.connect(zoonin,QtCore.SIGNAL('clicked()'), self.mainwd.zoomin)
		self.connect(zoonout,QtCore.SIGNAL('clicked()'), self.mainwd.zoomout)
		self.connect(getsvg,QtCore.SIGNAL('clicked()'), self.mainwd.getsvg)
		self.connect(setx,QtCore.SIGNAL('clicked()'), self.mainwd.setx)
		self.connect(close,QtCore.SIGNAL('clicked()'), self.close)
	
	def readfile(self,filename):
		self.mainwd.readfile(filename)
		self.setWindowTitle(filename + ' :: Rastrview')
	def close(self):
		self.accept()

class odoutput:
	def __init__(self):
		self.filename	= ""
		self.format		= ""
		self.conn		= 0
		self.watch		= ""
		self.id			= None

class outputglg(QtGui.QDialog):
	def __init__(self, odout = None , parent=None):
		super(outputglg, self).__init__()
		if odout == None:
			self.odoutput = odoutput()
		else:
			self.odoutput = odout
		self.fnameedit = QtGui.QLineEdit(self.odoutput.filename)
		self.formatcombo = QtGui.QComboBox(self)
		self.formatcombo.addItems(["excel","data","excel-tab","xml"])
		id = self.formatcombo.findText(self.odoutput.format)
		if id < 0:id = 0
		self.formatcombo.setCurrentIndex(id)

		self.watchcombo = QtGui.QComboBox(self)
		self.watchcombo.addItems( ["spikes","periods","last period","phases","time to spike","second correction"])
		id = self.watchcombo.findText(self.odoutput.watch)
		if id < 0:id = 0
		self.watchcombo.setCurrentIndex(id)
		self.conck = QtGui.QCheckBox("To hold an connctions spikes")
		if self.odoutput.conn:
			self.conck.setCheckState(QtCore.Qt.Checked)
		else:
			self.conck.setCheckState(QtCore.Qt.Unchecked)
		
		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)

		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("File:"))
		hbox01.addWidget(self.fnameedit)
		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(QtGui.QLabel("Format:"))
		hbox02.addWidget(self.formatcombo)
		hbox02.addStretch(1)
		hbox02.addWidget(QtGui.QLabel("Watch:"))
		hbox02.addWidget(self.watchcombo)
		hbox02.addStretch(1)
		hbox02.addWidget(self.conck)
		hbox02.addStretch(1)
		hbox02.addWidget(okButton)
		hbox02.addWidget(cancelButton)
		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox02)
		self.setLayout(vbox)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(self.conck, QtCore.SIGNAL('stateChanged (int)'), self.setOut)
	def readod(self,odout = None):
		if odout != None:
			self.odoutput = odout
		self.fnameedit.setText(self.odoutput.filename)
		id = self.formatcombo.findText(self.odoutput.format)
		if id < 0:id = 0
		self.formatcombo.setCurrentIndex(id)
		id = self.watchcombo.findText(self.odoutput.watch)
		if id < 0:id = 0
		self.watchcombo.setCurrentIndex(id)
		if self.odoutput.conn:
			self.conck.setCheckState(QtCore.Qt.Checked)
		else:
			self.conck.setCheckState(QtCore.Qt.Unchecked)
			
	def ok(self):
		self.odoutput.filename = self.fnameedit.text().toUtf8().data()
		self.odoutput.format = self.formatcombo.currentText().toUtf8().data()
		self.odoutput.watch = self.watchcombo.currentText().toUtf8().data()
		self.accept()

	def cancel(self):
		self.reject()
		
		
	def setOut(self,item):
		if item != 2:
			self.odoutput.conn = 0
		else:
			self.odoutput.conn = 1

class gloutput:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "output"
		insertout = QtGui.QAction(QtGui.QIcon(':/rastrt.png'), 'Insert or Edit Output', mainwnd)
		#insertppl.setShortcut('Meta+C')
		insertout.setStatusTip('Insert or Edit Connection')
		mainwnd.connect(insertout, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('&Output')
		menu.addAction(insertout)
		toolbar.addAction(insertout)
		self.ischanged	= False
		self.outlst = []
	def clean(self):
		self.ischanged	= False
		del self.outlst
		self.outlst = []
	def insert(self):
		if not self.parent.isactive : return
		item = self.mainwnd.tree.currentItem()
		ed = outputglg(parent = self.mainwnd)

		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			outid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes output item((("
			else:
				ed.readod(odout=self.outlst[outid])
		if not ed.exec_(): return
		self.ischanged	= True
		if ok :
			self.outlst[outid] = ed.odoutput
			item.setText(2,ed.odoutput.watch)
		else:
			newout = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newout)
			newout.setIcon(0,QtGui.QIcon(':/rastrt.png'))
			newout.setText(1,'Output:')
			newout.setText(2,ed.odoutput.watch)
			newout.setData(1,QtCore.Qt.UserRole,self.object)
			newout.setData(2,QtCore.Qt.UserRole,len(self.outlst))
			ed.odoutput.id = newout
			self.outlst.append(ed.odoutput)

	def remove(self,item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		outid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.outlst) <= outid : return
		self.outlst[outid].id = None
		self.ischanged	= True

	def click(self):
		self.insert()
	def getfilename(self,odout):
		if len(odout.filename) > 3:
			if odout.format == "xml":
				if odout.filename[-4:] != ".xml" :
					return odout.filename+".xml"
				else: return odout.filename
			elif odout.format == "data":
				if odout.filename[-4:] != ".dat" :
					return odout.filename+".dat"
				else: return odout.filename
			else:
				if odout.filename[-4:] != ".csv" :
					return odout.filename+".csv"
				else: return odout.filename
		else:
			if self.parent.filename[-4:] == ".pxm":
				return self.parent.filename[:-4]+"-"+odout.watch+".csv"
			else:
				return self.parent.filename+"-"+odout.watch+".csv"
				

			
	def save(self):
		result = []
		for out in self.outlst:
			if out.id == None: continue
			filename = 	self.getfilename(out)
			prn = "<output name=\"%s\" format=\"%s\" watch=\"%s\" "%(filename,out.format, out.watch)
			if out.conn == 0:
				prn += " connections = \"off\" "
			prn += " />"
			result.append(prn)
		self.ischanged	= False
		return result
	def startpoint(self, name, attr={}):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag\n <%s> !"%name,QtGui.QMessageBox.Ok,0)
			return
		odout = odoutput()
		if attr.get("name", -1) != -1:odout.filename = attr["name"]
		if attr.get("format",-1) != -1:odout.format = attr["format"]
		if attr.get("watch",-1) != -1:odout.watch = attr["watch"]
		if attr.get("connections",-1) != -1:
			if attr["connections"] == "off":
				odout.conn = 0
			else:
				odout.conn = 1
		else:
			odout.conn = 0
		newout = QtGui.QTreeWidgetItem(self.parent.root)
		self.parent.root.addChild(newout)
		newout.setIcon(0,QtGui.QIcon(':/rastrt.png'))
		newout.setText(1,'Output:')
		newout.setText(2,odout.watch)
		newout.setData(1,QtCore.Qt.UserRole,self.object)
		newout.setData(2,QtCore.Qt.UserRole,len(self.outlst))
		odout.id = newout
		self.outlst.append(odout)
		
	def stoppoint(self,name):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag end\n <%s> !"%name,QtGui.QMessageBox.Ok,0)
	def show(self):
		for out in self.outlst:
			if out.watch != "spikes": continue
			if out.format != "excel": continue
			if out.id == None: continue
			filename = self.getfilename(out)
			edt = glraster()
			edt.readfile(filename)
			edt.show()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	ex = glraster()
	ex.mainwd.readfile(sys.argv[-1])
	ex.show()
	#ex=prcviewdlg(prc)
	#ex.exec_()
	app.exec_()
