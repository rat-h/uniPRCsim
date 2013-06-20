##################################
#
# glphasetable.py
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
import string as str
import icons
import csv,sys,os

def streadyphasexctrator(filename = None):
	if filename == None: return None
	#if 
	fd = open(filename, "r")
	if fd == None: return None
	datai		= csv.reader(fd)
	names		= None
	timespikes	= None
	phases = None
	for row in datai:
		if len(row) < 2: continue
		if names == None:
			names = row[2:]
			timespikes = [ [0,0] for a in names ]
			phases = [ [ 0 for a in names] for b in names ]
			continue
		time = float(row[0])
		spikes = [ int(a) for a in row[2:] ]
		for ind in xrange(len(spikes)):
			if spikes[ind] == 1:
				timespikes[ind][0] = timespikes[ind][1]
				timespikes[ind][1] = time
				for a in xrange(len(spikes)):
					if timespikes[a][1] == timespikes[a][0]: continue
					phases[a][ind] = (time - timespikes[a][1])/(timespikes[a][1] - timespikes[a][0])
	return (names, phases)

class glphasetable(QtGui.QDialog):
	def __init__(self, parent=None, filename=None):
		tabl = streadyphasexctrator(filename)
		if tabl == None:
			QtGui.QMessageBox.critical(parent,"Critical ERROR!","Cannot open file %s!"%filename,QtGui.QMessageBox.Ok,0)
			self.reject()
		super(glphasetable, self).__init__()
		self.tbl = QtGui.QTableWidget()
		self.tbl.setRowCount( len(tabl[0]) )
		self.tbl.setColumnCount(len(tabl[0]) )
		self.tbl.setHorizontalHeaderLabels(tabl[0])
		self.tbl.setVerticalHeaderLabels(tabl[0])
		for findex in xrange(len(tabl[0])):
			for tindex in xrange(len(tabl[0])):
				item = QtGui.QTableWidgetItem("%f"%tabl[1][findex][tindex])
				item.setData(1,tabl[1][findex][tindex])
				self.tbl.setItem(findex,tindex,item)

		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.tbl)
		self.setLayout(vbox)
		self.update()





if __name__ == "__main__":
	if len(sys.argv) < 2:
		sys.stderr.write("USAGE: %s CSV-file\n"%sys.argv[0])
		sys.exit(1)
	tbl = streadyphasexctrator(sys.argv[1])
	if tbl == None:
		sys.stderr.write("Error with file object\n")
		sys.exit(1)
	for top in tbl[0]: print ",%s"%top,
	print
	for fidx in xrange(len(tbl[0])):
		print tbl[0][fidx],
		for tidx in xrange(len(tbl[0])):
			print ",%f"%tbl[1][fidx][tidx],
		print
