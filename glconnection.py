##################################
#
# glconnection.py
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
from PyQt4 import QtGui, QtCore
import icons
class odconnection:
	def __init__(self):
		self.name	= ""
		self.id		= None
		self.gsyn	= 0.0
		self.frm	= ""
		self.to		= ""
		self.prc	= ""
		self.delay	= -1.0
		self.jitter	= -1.0

class cnntedt(QtGui.QDialog):
	def __init__(self, cnnt=None, parent=None, frmto=None, prcs=None):
		super(cnntedt, self).__init__()
		self.cnnt = cnnt
		if self.cnnt == None :
			self.cnnt = odconnection()
		self.setWindowTitle(self.cnnt.name + ' :: Connection Editor')
		self.nameedit = QtGui.QLineEdit(self.cnnt.name)
		self.gsynedit = QtGui.QDoubleSpinBox(self)
		self.gsynedit.setValue(self.cnnt.gsyn)
		self.gsynedit.setMaximum(1000000000.0)
		self.gsynedit.setMinimum(0.0)
		self.gsynedit.setDecimals(10)
		self.gsynedit.setSingleStep(0.01)
		self.frm = QtGui.QComboBox(self)
		self.frm .addItems(frmto)
		self.frm .setEditable(False)
		id = self.frm.findText(self.cnnt.frm)
		if id < 0:id = 0
		self.frm.setCurrentIndex(id)
		self.to = QtGui.QComboBox(self)
		self.to .addItems(frmto)
		self.to .setEditable(False)
		id = self.frm.findText(self.cnnt.to)
		if id < 0:id = 0
		self.to .setCurrentIndex(id)
		self.prc = QtGui.QComboBox(self)
		self.prc .addItems(prcs)
		self.prc .setEditable(False)
		id = self.prc.findText(self.cnnt.prc)
		if id < 0:id = 0
		self.prc .setCurrentIndex(id)
		self.delck = QtGui.QCheckBox("Set Dalay in...")
		self.deledit = QtGui.QDoubleSpinBox(self)
		self.deledit.setValue(self.cnnt.delay)
		self.deledit.setMaximum(1000000000.0)
		self.deledit.setMinimum(0.0)
		self.deledit.setDecimals(10)
		self.deledit.setSingleStep(0.0001)
		self.jitterck = QtGui.QCheckBox("Set Jitter in...")
		self.jitteredit = QtGui.QDoubleSpinBox(self)
		self.jitteredit.setValue(self.cnnt.jitter)
		self.jitteredit.setMaximum(1000000000.0)
		self.jitteredit.setMinimum(0.0)
		self.jitteredit.setDecimals(10)
		self.jitteredit.setSingleStep(0.0001)
		if self.cnnt.delay < 0.0:
			self.delck.setCheckState(QtCore.Qt.Unchecked)
			self.deledit.setVisible(False)
			self.jitterck.setVisible(False)
			self.jitteredit.setVisible(False)
		elif self.cnnt.delay >= 0.0 and self.cnnt.jitter < 0.0:
			self.delck.setCheckState(QtCore.Qt.Checked)
			self.deledit.setVisible(True)
			self.jitterck.setCheckState(QtCore.Qt.Unchecked)
			self.jitteredit.setVisible(False)
		
		
		okButton	 = QtGui.QPushButton(QtGui.QIcon(':/dialog-ok.png'),"&OK",self)
		cancelButton = QtGui.QPushButton(QtGui.QIcon(':/dialog-cancel.png'),"&Cancel",self)
		hbox01 = QtGui.QHBoxLayout()
		hbox01.addWidget(QtGui.QLabel("Name:"))
		hbox01.addWidget(self.nameedit)
		hbox01.addWidget(QtGui.QLabel("G syn:"))
		hbox01.addWidget(self.gsynedit)
		hbox01.addStretch(1)
		hbox01.addWidget(okButton)
		hbox01.addWidget(cancelButton)

		hbox02 = QtGui.QHBoxLayout()
		hbox02.addWidget(QtGui.QLabel("From:"))
		hbox02.addWidget(self.frm)
		hbox02.addStretch(1)
		hbox02.addWidget(QtGui.QLabel("To:"))
		hbox02.addWidget(self.to)
		hbox02.addStretch(1)
		hbox02.addWidget(QtGui.QLabel("PRC:"))
		hbox02.addWidget(self.prc)

		hbox03 = QtGui.QHBoxLayout()
		hbox03.addWidget(self.delck)
		hbox03.addWidget(self.deledit)
		hbox03.addStretch(1)
		hbox03.addWidget(self.jitterck)
		hbox03.addWidget(self.jitteredit)

		vbox = QtGui.QVBoxLayout()
		vbox.addLayout(hbox01)
		vbox.addLayout(hbox02)
		vbox.addLayout(hbox03)
		self.setLayout(vbox)
		self.connect(okButton, QtCore.SIGNAL('clicked()'), self.ok)
		self.connect(cancelButton, QtCore.SIGNAL('clicked()'), self.cancel)
		self.connect(self.delck, QtCore.SIGNAL('stateChanged (int)'), self.setDelay)
		self.connect(self.jitterck, QtCore.SIGNAL('stateChanged (int)'), self.setJitter)
		self.connect(self.nameedit, QtCore.SIGNAL('editingFinished()'), self.rename)
	def rename(self):
		if self.cnnt == None :
			self.cnnt = odconnection()
		self.cnnt.name = self.nameedit.text()
		self.setWindowTitle(self.cnnt.name + ' :: Connection Editor')

	def readcnnt(self, cnnt=None):
		if cnnt != None:
			self.cnnt = cnnt
		self.setWindowTitle(self.cnnt.name + ' :: Connection Editor')
		self.nameedit.setText(self.cnnt.name)
		self.gsynedit.setValue(self.cnnt.gsyn)
		id = self.frm.findText(self.cnnt.frm)
		if id < 0:id = 0
		self.frm.setCurrentIndex(id)
		id = self.frm.findText(self.cnnt.to)
		if id < 0:id = 0
		self.to .setCurrentIndex(id)
		id = self.prc.findText(self.cnnt.prc)
		if id < 0:id = 0
		self.prc .setCurrentIndex(id)
#		print "> Delay value: ", self.cnnt.delay
#		print "> Jitter value: ", self.cnnt.jitter
		if self.cnnt.delay < 0.0:
			self.delck.setCheckState(QtCore.Qt.Unchecked)
			self.deledit.setVisible(False)
			self.jitterck.setVisible(False)
			self.jitteredit.setVisible(False)
		elif self.cnnt.delay >= 0.0 and self.cnnt.jitter < 0.0:
			self.delck.setCheckState(QtCore.Qt.Checked)
			self.jitterck.setCheckState(QtCore.Qt.Unchecked)
			self.deledit.setVisible(True)
			self.jitteredit.setVisible(False)
			self.deledit.setValue(self.cnnt.delay)
		else :
			self.jitterck.setCheckState(QtCore.Qt.Checked)
			self.delck.setCheckState(QtCore.Qt.Checked)
			self.deledit.setVisible(True)
			self.jitteredit.setVisible(True)
			self.deledit.setValue(self.cnnt.delay)
			self.jitteredit.setValue(self.cnnt.jitter)
		
	
	def setDelay(self, cond):
		if cond != 2:
			self.deledit.setVisible(False)
			self.jitterck.setCheckState(QtCore.Qt.Unchecked)
			self.jitteredit.setVisible(False)
			self.jitterck.setVisible(False)
			self.cnnt.delay = -1.0
			self.cnnt.jitter	= -1.0
		else:
			self.deledit.setVisible(True)
			if self.cnnt.delay < 0.0 : self.cnnt.delay = 10.0
			self.deledit.setValue(self.cnnt.delay)
			if self.cnnt.jitter < 0:
				self.jitterck.setVisible(True)
				self.jitterck.setCheckState(QtCore.Qt.Unchecked)
				self.jitteredit.setVisible(False)
			else:
				self.jitterck.setVisible(True)
				self.jitterck.setCheckState(QtCore.Qt.Checked)
				self.jitteredit.setVisible(True)
				self.jitteredit.setValue(self.cnnt.jitter)
			
	def setJitter(self, cond):
		if self.cnnt.delay < 0.0: return
		if cond != 2:
			self.jitteredit.setVisible(False)
			self.cnnt.jitter	= -1.0
		else:
			self.jitteredit.setVisible(True)
			if self.cnnt.jitter < 0.0 :self.cnnt.jitter	= 1.0
			self.jitteredit.setValue(self.cnnt.jitter)
		
	def ok(self):
		self.cnnt.name = self.nameedit.text().toUtf8().data()
		if len(self.cnnt.name) < 1:
			QtGui.QMessageBox.critical(self,"Critical ERROR!"," You should specify the connection name! ",QtGui.QMessageBox.Ok,0)
			return
		self.cnnt.gsyn = self.gsynedit.value()
		self.cnnt.frm = self.frm.currentText().toUtf8().data()
		self.cnnt.to = self.to.currentText().toUtf8().data()
		self.cnnt.prc = self.prc.currentText().toUtf8().data()
		if self.delck.checkState() != 2:
			self.cnnt.delay = -1.0
			self.cnnt.jitter = -1.0
		elif self.jitterck.checkState() != 2:
			self.cnnt.delay = self.deledit.value()
			self.cnnt.jitter = -1.0
		else:
			self.cnnt.delay = self.deledit.value()
			self.cnnt.jitter = self.jitteredit.value()
#		print "< Delay value: ", self.cnnt.delay
#		print "< Jitter value: ", self.cnnt.jitter
		self.accept()
	def cancel(self):
		self.reject()




class glconnection:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "connection"
		insertppl = QtGui.QAction(QtGui.QIcon(':/connection.png'), 'Insert Connection', mainwnd)
		insertppl.setShortcut('Meta+C')
		insertppl.setStatusTip('Insert Connection')
		mainwnd.connect(insertppl, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('&Connection')
		menu.addAction(insertppl)
		toolbar.addAction(insertppl)
		self.ischanged	= False
		self.cnntlst = []
	def clean(self):
		self.ischanged	= False
		del self.cnntlst
		self.cnntlst = []
	def insert(self):
		if not self.parent.isactive : return
		frmto=self.parent.getnames(lst=["population","neurons","noisyneurons"])
		if len(frmto) < 1:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!"," You should have at least one neurons set or population! ",QtGui.QMessageBox.Ok,0)
			return
		prcs=self.parent.getnames(lst=["prc","rprc"])	
		if len(prcs) < 1:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!"," You should have at least one PRC function! ",QtGui.QMessageBox.Ok,0)
			return
		edit = cnntedt(parent = self.mainwnd, frmto=frmto, prcs=prcs)
		item = self.mainwnd.tree.currentItem()
		ok = False
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			cnntid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes Connection item((("
			else:
				edit.readcnnt(cnnt=self.cnntlst[cnntid])
		if not edit.exec_(): return
		self.ischanged	= True
		if ok :
			self.cnntlst[cnntid] = edit.cnnt
			item.setText(2,edit.cnnt.name)
		else:
			newcnnt = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newcnnt)
			newcnnt.setIcon(0,QtGui.QIcon(':/connection.png'))
			newcnnt.setText(1,'Connection:')
			newcnnt.setText(2,edit.cnnt.name)
			newcnnt.setData(1,QtCore.Qt.UserRole,self.object)
			newcnnt.setData(2,QtCore.Qt.UserRole,len(self.cnntlst))
			edit.cnnt.id = newcnnt
			self.cnntlst.append(edit.cnnt)
		
	def remove(self,item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		cnntid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.cnntlst) <= cnntid : return
		self.cnntlst[cnntid].id = None
		self.ischanged	= True

	def click(self):
		self.insert()
	def save(self):
		result = []
		for cnnt in self.cnntlst:
			if cnnt.id == None: continue
			if cnnt.delay < 0.0:
				result.append("<connection name=\"%s\" from=\"%s\" to=\"%s\" gsyn=\"%g\" prc=\"%s\" />"%(cnnt.name, cnnt.frm, cnnt.to, cnnt.gsyn, cnnt.prc) )
			elif cnnt.jitter < 0.0:
				result.append("<connection name=\"%s\" from=\"%s\" to=\"%s\" gsyn=\"%g\" prc=\"%s\" delay=\"%g\" />"%(cnnt.name, cnnt.frm, cnnt.to, cnnt.gsyn, cnnt.prc, cnnt.delay) )
			else:
				result.append("<connection name=\"%s\" from=\"%s\" to=\"%s\" gsyn=\"%g\" prc=\"%s\" delay=\"%g\" jitter=\"%g\" />"%(cnnt.name, cnnt.frm, cnnt.to, cnnt.gsyn, cnnt.prc, cnnt.delay, cnnt.jitter) )
		return result
	def startpoint(self, name, attr={}):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag\n <%s> !"%name,QtGui.QMessageBox.Ok,0)
			return
		if attr.get("name", 0) == 0 or attr.get("gsyn",0.0) == 0 or attr.get("from", 0) == 0 or attr.get("to", 0) == 0 or attr.get("prc", 0) == 0:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Tag <%s> should have attributes\n name - from - to - gsym - prc!"%name,QtGui.QMessageBox.Ok,0)
		tmpcnnt = odconnection()
		tmpcnnt.name = attr["name"]
		tmpcnnt.gsyn = float(attr["gsyn"])
		tmpcnnt.frm = attr["from"]
		tmpcnnt.to = attr["to"]
		tmpcnnt.prc = attr["prc"]
		if attr.get("delay",0):
			tmpcnnt.delay = float(attr["delay"])
		if attr.get("jitter",0):
			tmpcnnt.jitter = float(attr["jitter"])

		newcnnt = QtGui.QTreeWidgetItem(self.parent.root)
		self.parent.root.addChild(newcnnt)
		newcnnt.setIcon(0,QtGui.QIcon(':/connection.png'))
		newcnnt.setText(1,'Connection:')
		newcnnt.setText(2,tmpcnnt.name)
		newcnnt.setData(1,QtCore.Qt.UserRole,self.object)
		newcnnt.setData(2,QtCore.Qt.UserRole,len(self.cnntlst))
		tmpcnnt.id = newcnnt
		self.cnntlst.append(tmpcnnt)
		return

		
		
	def stoppoint(self,name):
		if name != self.object:
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag end\n <%s> !"%name,QtGui.QMessageBox.Ok,0)

