import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit,QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My cool first GUI")#to set the name of the window 
        self.setGeometry(700, 300, 400, 400)#to set the position and the size of the window in the screen using (x, y, height, width) format
        self.line_edit = QLineEdit(self) #we use this to create a text box thats an object that belong to the class
        self.Button_Edit = QPushButton("Submit", self)
        self.initUI()
        
        
#We are going to practice how to use textbox and LineEdit
    def initUI(self):
        self.line_edit.setGeometry(10,10,200,40)
        self.line_edit.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")
        self.Button_Edit.setGeometry(210,10,100,40)
        self.Button_Edit.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")
        
        self.Button_Edit.clicked.connect(self.Submit)
        
    def Submit(self):
        print("You have clicked the button")


def main():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    window = MainWindow()
    window.show() #this is to enable the window to show bcoz its default setting is to hide the window
    sys.exit(app.exec())#The "exec_()" is to enable to stay open and execute code/task till the user closes it
    

if __name__ =="__main__":
    main()