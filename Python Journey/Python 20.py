import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit,QPushButton
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My cool first GUI")#to set the name of the window 
        self.setGeometry(700, 300, 400, 400)#to set the position and the size of the window in the screen using (x, y, height, width) format
        self.line_edit = QLineEdit(self) #we use this to create a text box thats an object that belong to the class
        self.Button_Edit = QPushButton("Submit", self)
        #now we work on designing a button
        self.button1 = QPushButton("#1")
        self.button2 = QPushButton("#2")
        self.button3 = QPushButton("#3")
        #This is a function thats used to edit user interface
        self.initUI()
        
        
#We are going to practice how to use textbox and LineEdit
    """def initUI(self):
        self.line_edit.setGeometry(10,10,200,40)
        self.line_edit.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")
        self.Button_Edit.setGeometry(210,10,100,40)
        self.Button_Edit.setStyleSheet("font-size: 25px;"
                                     "font-family: Arial")
        
        self.line_edit.setPlaceholderText("Enter your name")#to set a place holder text for the textbox
        self.Button_Edit.clicked.connect(self.Submit) #to connect the button to the function
    
    #This is the function to store and make use the text in the text box
    def Submit(self):
        text = self.line_edit.text()
        print(f"Hello {text}")"""



#__________________________________________________________________________________________________________________________________________________________________________________________________
#Now we are going to work with widgets and css  template to design button
    def initUI(self):
    #Since we cant add QBoxLayout to the QMainWindow directly, we would create external 
    # widget for QBoxLayout and then place the widget in the QBoxLayout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        hbox = QHBoxLayout()
        
        hbox.addWidget(self.button1)
        hbox.addWidget(self.button2)
        hbox.addWidget(self.button3)
        
        central_widget.setLayout(hbox)
        #Instead styling each button separately we are gonna style everything together
        
        #to apply individual distinct style to each button we can redefine the name
        self.button1.setObjectName("button1")
        self.button2.setObjectName("button2")
        self.button3.setObjectName("button3")
        
        self.setStyleSheet("""
                           QPushButton{
                               font-size: 40px;
                               font-family: Arial;
                               padding: 15px 75px;
                               margin: 25px;
                               border: 3px solid;
                               border-radius: 15px;
                           }
                            QPushButton#button1{
                               background-color: red; 
                           }
                           QPushButton#button2{
                               background-color: green;
                           }
                           QPushButton#button3{
                               background-color: blue;
                           }
                           QPushButton#button1:hover{
                               background-color: #f57e69; 
                           }
                           QPushButton#button2:hover{
                               background-color: #4fc478;
                           }
                           QPushButton#button3:hover{
                               background-color: #53a9db;
                           }
                           """)#we can also use color code e.g #7a9acf
        
        

def main():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    window = MainWindow()
    window.show() #this is to enable the window to show bcoz its default setting is to hide the window
    sys.exit(app.exec())#The "exec_()" is to enable to stay open and execute code/task till the user closes it
    

if __name__ =="__main__":
    main()