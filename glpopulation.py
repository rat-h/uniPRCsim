##################################
#
# glpopulation.py
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
import glneurons
import icons

class odpopulation:
	def __init__(self):
		self.name	= ""
		self.id		= None
		self.pid	= -1


class glpopulation:
	def __init__(self,parent = None, mainwnd = None, menubar = None, toolbar = None):
		self.parent		= parent
		self.mainwnd	= mainwnd
		self.object		= "population"
		insertppl = QtGui.QAction(QtGui.QIcon(':/population.png'), 'Insert/Edit Population', mainwnd)
		insertppl.setShortcut('Ctrl+L')
		insertppl.setStatusTip('Insert Population')
		mainwnd.connect(insertppl, QtCore.SIGNAL('triggered()'), self.insert)
		menu = menubar.addMenu('&Population')
		menu.addAction(insertppl)
		toolbar.addAction(insertppl)
		self.ischanged	= False
		self.poplst = []
		self.tmppop = None
	def clean(self):
		del self.poplst
		self.poplst = []
		self.tmppop = None
		self.ischanged	= False
	def insert(self):
		if not self.parent.isactive : return
		item = self.mainwnd.tree.currentItem()
		ok = False
		edit = QtGui.QInputDialog(self.mainwnd)
		edit.setLabelText("Insert New name for population:")
		if item.data(1,QtCore.Qt.UserRole) == self.object:
			popid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
			if not ok:
				print "Collapes POP item((("
			else:
				edit.setTextValue(self.poplst[popid].name)
		if ok:
			if edit.exec_():
				if edit.textValue().length() < 1:
					QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!"," You should specify the name of population ",QtGui.QMessageBox.Ok,0)
					return
				self.poplst[popid].name = edit.textValue().toUtf8().data()
				item.setText(2,self.poplst[popid].name)
		else:
			if not edit.exec_(): return
			if edit.textValue().length() < 1:
				QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!"," You should specify the name of population ",QtGui.QMessageBox.Ok,0)
				return
			newpop = QtGui.QTreeWidgetItem(self.parent.root)
			self.parent.root.addChild(newpop)
			newpop.setIcon(0,QtGui.QIcon(':/population.png'))
			newpop.setText(1,'Population:')
			newpop.setText(2,edit.textValue())
			newpop.setData(1,QtCore.Qt.UserRole,self.object)
			newpop.setData(2,QtCore.Qt.UserRole,len(self.poplst))
			pop = odpopulation()
			pop.id = newpop
			pop.name = edit.textValue().toUtf8().data()
			pop.pid = len(self.poplst)
			self.poplst.append(pop)
			
		self.ischanged	= True

	def remove(self,item):
		if item.data(1,QtCore.Qt.UserRole) != self.object: return
		popid, ok = item.data(2,QtCore.Qt.UserRole).toInt()
		if not ok: return
		if len(self.poplst) <= popid : return
		#del self.poplst[popid].nrn
		self.poplst[popid].id = None
		self.ischanged	= True
	def click(self):
		self.insert()
	def save(self):
		result=[]
		for pop in self.poplst:
			if pop.id == None: continue
			result.append("<population name=\"%s\">"%pop.name)
			for prn in self.parent.glneurons.save(pid= pop.pid):
				result.append("\t"+prn)
			result.append("</population>")
		self.ischanged	= False
		return result
	def startpoint(self,name,attr={}):
		if self.tmppop == None and name == self.object:
			self.tmppop = odpopulation()
			if attr.get("name",0):
				self.tmppop.name=attr["name"]
			self.tmppop.id = QtGui.QTreeWidgetItem(self.parent.root)
			self.tmppop.id.setIcon(0,QtGui.QIcon(':/population.png'))
			self.tmppop.id.setText(1,'Population:')
			self.tmppop.id.setText(2,self.tmppop.name)
			self.tmppop.id.setData(1,QtCore.Qt.UserRole,self.object)
			self.tmppop.id.setData(2,QtCore.Qt.UserRole,len(self.poplst))
		elif self.tmppop != None:
			self.parent.glneurons.startpoint(name, attr=attr, pid=len(self.poplst) )
		else :
			QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected tag\n <%s> !"%name,QtGui.QMessageBox.Ok,0)
			
		return
	def stoppoint(self,name):
		if self.tmppop != None and name == self.object:
			self.parent.root.addChild(self.tmppop.id)
			self.tmppop.pid = len(self.poplst)
			self.poplst.append(self.tmppop)
			self.tmppop = None
			return
		elif self.tmppop != None and name != self.object:
			self.parent.glneurons.stoppoint(name)
			return
		QtGui.QMessageBox.critical(self.mainwnd,"Critical ERROR!","Bad or unexpected closed tag\n <%s> !"%name,QtGui.QMessageBox.Ok,0)
	def getnames(self):
		return [ x.name for x in self.poplst]
		
