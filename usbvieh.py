#!/usr/bin/python

import sys
import os
from PyQt4 import QtGui, QtCore
from subprocess import call
import pickle

class Usbvieh(QtGui.QWidget):
    def __init__(self):
        super(Usbvieh, self).__init__()
        self.config=os.path.expanduser('~/.usbvieh')
        self.storage=os.path.expanduser('~/MyDocs/usbvieh/')
        self.filelist = dirList=os.listdir(self.storage)
        try:
            f=open(self.config,'r')
            self.selected_files = pickle.load(f)
            f.close()
        except IOError: # no such file
            self.selected_files=[]
        except EOFError: # empty file
            self.selected_files=[]
        self.init_gui()

    def unload_modules(self):
        call(["sudo", "modprobe", "-r", "g_ether"])
        call(["sudo", "modprobe", "-r", "g_file_storage"])

    def load_ether(self):
        self.unload_modules()
        call(["sudo", "modprobe", "g_ether"])

    def load_file_storage(self):
        #with open('...') as f: is python 2.6
        f=open('/etc/modprobe.d/g_file_storage', 'w')
        f.write("options g_file_storage file="+self.storage+(','+self.storage).join(self.selected_files)+'\n')
        f.close()
        f=open(self.config,'w')
        pickle.dump(self.selected_files,f)
        f.close()
        self.unload_modules()
        call(["sudo", "modprobe", "g_file_storage"])

    def update_lbl2(self):
        self.lbl2.setText('\n'.join(self.selected_files))

    def clear_filelist(self):
        self.selected_files = []
        self.update_lbl2()

    def add_file(self):
        if len(self.lst.selectedIndexes()):
            self.selected_files += [self.filelist[self.lst.selectedIndexes()[0].row()]]
        self.update_lbl2()

    def init_gui(self):

        self.setWindowTitle('usbvieh')

        btn_ether = QtGui.QPushButton('ether', self)
        btn_ether.resize(130, 90)
        btn_ether.move(20, 180)  
        QtCore.QObject.connect(btn_ether, QtCore.SIGNAL('clicked()'), self.load_ether)

        btn_file = QtGui.QPushButton('file', self)
        btn_file.resize(130, 90)
        btn_file.move(20, 80)  
        QtCore.QObject.connect(btn_file, QtCore.SIGNAL('clicked()'), self.load_file_storage)

        lbl0 = QtGui.QLabel('load\nmodule:', self)
        lbl0.move(15, 10)

        lbl1 = QtGui.QLabel('Selected files:', self)
        lbl1.move(175, 10)

        self.lbl2 = QtGui.QLabel('', self)
        self.lbl2.resize(470, 200)
        self.lbl2.move(175, 20)

        mdl = QtGui.QStringListModel(self.filelist)

        self.lst = QtGui.QListView(self)
        self.lst.resize(470, 200)
        self.lst.move(175, 190)
        self.lst.setModel(mdl)

        btn_clr = QtGui.QPushButton('clr', self)
        btn_clr.resize(130, 90)
        btn_clr.move(660, 50)  
        QtCore.QObject.connect(btn_clr, QtCore.SIGNAL('clicked()'), self.clear_filelist)

        btn_add = QtGui.QPushButton('+', self)
        btn_add.resize(130, 90)
        btn_add.move(660, 170)  
        QtCore.QObject.connect(btn_add, QtCore.SIGNAL('clicked()'), self.add_file)

        self.update_lbl2()
        self.show()
    

def main():
    app = QtGui.QApplication(sys.argv)
    usbvieh = Usbvieh()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

