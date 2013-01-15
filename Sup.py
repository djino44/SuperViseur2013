import sys
from PySide.QtCore import Qt, QSize,QObject
from PySide import QtCore, QtGui
from PySide.QtCore import QSettings,QSignalMapper
from PySide.QtGui import QWidget, QPushButton, QApplication, QFileDialog, QMessageBox
from graphSup import Ui_MainWindow
from Thread import commInter
i=0
j=0

tabSlider={}
tabDial={}
tabAna={}
tabTor={}

class MyMainWindow(QtGui.QMainWindow):
    
    clicked = QtCore.Signal(str)
    

    
    
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.ChargeConf)
        self.udp = commInter(1)
        self.udp.readyRead.connect(self.updateD)
        self.udp.start()

        self.ui.actionOuvrir.triggered.connect(self.ouvrirDialogue)
        self.signalMapper = QSignalMapper()
        self.signalMapper.mapped[QObject].connect(self.buttonClicked)
        self.settings = QSettings("toto.ini",QSettings.IniFormat)
        self.clicked.connect(self.click)
        
    def updateD(self,devType,devNum,devStatus):
        global tabAna, tabTor
        print(devType+devNum+devStatus)
        
        if devType=="A":
            numberA= int(devNum)
            val=devStatus
            labName=tabAna[numberA].objectName()
            tabAna[numberA].setText(labName+" :"+val)
        
        if devType=="T":
            print "TOR"
            numberT= int(devNum)
            valT=devStatus
            
            if valT=='1':
                print('valT=1')
                print numberT
                tabTor[numberT].setChecked(True)
            else: 
                print('valT=0')
                print numberT
                tabTor[numberT].setChecked(False)
        
                               
    def buttonClicked(self, button):
        global tabBtn
        
        if isinstance(button,QtGui.QCheckBox):
            print(button.isChecked())
            
        elif isinstance(button,QtGui.QDial):    
            print( button.value())
            label=tabDial[button]
            labName=label.objectName()
            label.setText(labName+" :"+str(button.value()))
                
        elif isinstance(button,QtGui.QSlider):
            print( button.value())
            label=tabSlider[button]
            labName=label.objectName()
            label.setText(labName+" :"+str(button.value()))            
            
       
                
    @QtCore.Slot(object)
    def click(self):
        
        button = self.sender()
       
        
        if isinstance(button,QtGui.QCheckBox):
            print(button.isChecked())
        
        elif isinstance(button,QtGui.QDial):    
            print (button.objectName(),button.value())
        
       
        #elif isinstance(button,QtGui.QSlider)
    
    
    
    def ChargeConf(self):
        global i
        global j
        global tabBtn,tabDial,tabAna,tabTor
        
        
        settings=self.settings
        settings.beginGroup("Voyants");
        keys = settings.childKeys()
        
         
        for x in keys:
             button = QtGui.QCheckBox()           
             self.ui.gridLayout_1.addWidget(button,i,j)
             button.setVisible(True)
             j=j+1
             if (j>1):
                j=0
                i=i+1
             button.setText(settings.value(x))
             #button.stateChanged.connect(self.click)
             button.setObjectName(settings.value(x))
             button.stateChanged.connect(self.signalMapper.map)
             self.signalMapper.setMapping(button, button) 
        settings.endGroup()
        
        
        i=j=0
        settings.beginGroup("TOR");
        keys = settings.childKeys()
        
        for z in keys:
            button = QtGui.QRadioButton()
            button.setAutoExclusive(False)
            print z
            tabTor[int(z)]=button
            self.ui.gridLayout_3.addWidget(button,i,j)
            button.setVisible(True)
                      
            j=j+1
            if (j>1):
                j=0
                i=i+1
            button.setText(settings.value(z))
            button.setObjectName(settings.value(z)) 
            #button.pressed.connect(self.click)
            button.pressed.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button)    
        
        settings.endGroup()
        
        
        
        i=j=0
        settings.beginGroup("ANA");
        keys = settings.childKeys()
        for e in keys:
            button = QtGui.QLabel()
            tabAna[int(e)]= button
            self.ui.gridLayout_2.addWidget(button,i,j)
            button.setVisible(True)
                      
            j=j+1
            if (j>1):
                j=0
                i=i+1
            button.setText(settings.value(e))
            button.setObjectName(settings.value(e))    
        
        settings.endGroup()
        
        
        
        i=j=0
        settings.beginGroup("SERVOS");
        keys = settings.childKeys()
        for r in keys:
            button = QtGui.QDial()
          
            
            label= QtGui.QLabel()
            label.setObjectName(settings.value(r))
            label.setText(label.objectName()+" :"+str(button.value()))
            
            self.ui.gridLayout_4.addWidget(button,i,j)
            j+=1
            self.ui.gridLayout_4.addWidget(label,i,j)
            button.setVisible(True)
            label.setVisible(True)
                      
            
            j=0
            i+=1
            button.setRange(-90,90) 
            button.setObjectName(settings.value(r))    
            
            
            tabDial[button]=label
            button.valueChanged.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button)
            
        settings.endGroup()
        
        
        
        
        i=j=0
        settings.beginGroup("MOTORS");
        keys = settings.childKeys()
        for t in keys:
            button = QtGui.QSlider()
            button.setObjectName(settings.value(t))  
            button.setOrientation(Qt.Vertical)
            button.setRange(0,100)
            
            label= QtGui.QLabel()
            label.setObjectName(settings.value(t))
            label.setText(label.objectName()+" :"+str(button.value()))
            
            self.ui.gridLayout_6.addWidget(button,i,j)
            j+=1
            self.ui.gridLayout_6.addWidget(label,i,j)
            j+=1
            button.setVisible(True)
            label.setVisible(True)          
            if (j>3):
                j=0
                i=i+1
             
           
            tabSlider[button]=label
            button.valueChanged.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button)
            
        settings.endGroup()
        
        i=j=0
        settings.beginGroup("BOARDS");
        keys = settings.childKeys()
        
        for y in keys:
            button = QtGui.QRadioButton()
            self.ui.gridLayout_5.addWidget(button,i,j)
            button.setVisible(True)
                      
            j=j+1
            if (j>1):
                j=0
                i=i+1
            button.setText(settings.value(y))
            button.setObjectName(settings.value(y)) 
            #button.pressed.connect(self.click) 
            button.pressed.connect(self.signalMapper.map)
            self.signalMapper.setMapping(button, button)   
        
        settings.endGroup()
    
    
    
    
    
    
      
      
 
    
    def ouvrirDialogue(self):        
        
        fichier = QFileDialog.getOpenFileName(self,"Ouvrir un fichier","","Config (*.ini)")
        
        if fichier:
    
            self.DelGridLayout(self.ui.gridLayout_1)
            self.DelGridLayout(self.ui.gridLayout_2)
            self.DelGridLayout(self.ui.gridLayout_3)
            self.DelGridLayout(self.ui.gridLayout_4)
            self.DelGridLayout(self.ui.gridLayout_5)
            self.DelGridLayout(self.ui.gridLayout_6)

            #QMessageBox.information(self, "Fichier",u"Votre selection :\n" + fichier[0]);
            self.settings = QSettings(fichier[0], QSettings.IniFormat)
            self.settings.setFallbacksEnabled(False)
            try:
                self.ChargeConf()
            except:
                QMessageBox.information(self, "Mauvais Fichier", "");


    def DelGridLayout(self, lyt):
    
        for i in range(0, lyt.count()):
            lyt.itemAt(i).widget().close()
        
    
        
    def closeEvent(self, e):
       
        e.accept()      
        #self.udp.stop()
        self.udp._Thread__stop()
      
      
      
      
      
      
                             
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyMainWindow()
    myapp.show()
    sys.exit(app.exec_())
    