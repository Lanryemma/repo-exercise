#We will be working with Pyqt5.QtGui (Also know as python graphic user interface)
#now we will import what we need from the PyQt5 module
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon #to be able to work with icons
from PyQt5.QtGui import QFont #to be able to add font and font-size
from PyQt5.QtCore import Qt#to be able to align elements on the window and to create checkbox
from PyQt5.QtGui import QPixmap 
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout #To enable layout settings
from PyQt5.QtWidgets import QPushButton #to be to add interactive buttons
from PyQt5.QtWidgets import QRadioButton, QButtonGroup,QCheckBox #to create radio button and checkbox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My cool first GUI")#to set the name of the window 
        self.setGeometry(700, 300, 400, 400)#to set the position and the size of the window in the screen using (x, y, height, width) format
        self.setWindowIcon(QIcon("Python Journey/profile_pic.jpg"))#To set the provided picture as the icon
        self.button = QPushButton("Click me!",self)
        self.labell = QLabel("Hello",self)#label for the button demonstration
        self.checkbox = QCheckBox("Do you like food ?", self) #to create a checkbox that belong to the class
        self.radio1 = QRadioButton("Visa", self)
        self.radio2 = QRadioButton("Mastercard", self)
        self.radio3 = QRadioButton("Gift card", self)
        self.radio4 = QRadioButton("in store", self)
        self.radio5 = QRadioButton("Online", self)
        #we want radio 1-3 to be in one group and radio 4-5 in another group
        self.button_group1 = QButtonGroup(self)
        self.button_group2 = QButtonGroup(self)
        self.initUI()
        

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #now we will add labels
        """label  = QLabel("Hello!!",self)
        label.setFont(QFont("Arial", 40))#To set the font style and the font size
        label.setGeometry(0, 0, 400, 100)#to set the position and the size of the Label in the screen using (x, y, height, width) format
        #Now to add css like styling to our label by using the stylesheet method
        label.setStyleSheet("color: blue;"
                            "background-color: #7a9acf;"
                            "font-weight: bold;"
                            "font-style: italic;"
                            "text-decoration: underline;") #we could also use code colors like "#1a662b", "#1a246"""


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Now we align the label
        #  label.setAlignment(Qt.AlignTop) #align to the top vertically
        #  label.setAlignment(Qt.AlignBottom) #align to the bottom vertically
        #  label.setAlignment(Qt.AlignVCenter) #align to the center vertically
        
        #  label.setAlignment(Qt.AlignRight) #align to the right horizontally
        #  label.setAlignment(Qt.AlignHCenter) #align to the center horizontally
        #  label.setAlignment(Qt.AlignLeft) #align to the left horizontally
        
        #  label.setAlignment(Qt.AlignHCenter | Qt.AlignTop) #align to the center horizontally and top vertically
        #  label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom) #align to the center horizontally and Bottom vertically
        #  label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter) #align to the center horizontally and center vertically
        

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #we are going to add image to our window
        """label1 = QLabel(self)
        label1.setGeometry(0, 0, 200, 200)
        #now we use the pixmap method to map our image to the geometry coordinates
        pixmap1 = QPixmap("Python Journey/profile_pic.jpg")
        label1.setPixmap(pixmap1)
        
        #now to let the entire image scale to the size of our geometry values
        label1.setScaledContents(True)"""
        
        #to change the position of the image to different corners of the window
        #to position it at the top right corner of the screen
        #  label1.setGeometry(self.width() - label1.width(), 0, label1.width(),label1.height())
        
        #to position it at the bottom right corner of the screen
        #  label1.setGeometry(self.width() - label1.width(), self.height() - label1.height(), label1.width(),label1.height())
        
        #to position it at the bottom left corner of the screen
        #  label1.setGeometry(0, self.height() - label1.height(), label1.width(),label1.height())
        
        #to position it at the center of the window
        """label1.setGeometry(self.width() - label1.width() // 2, #the double slash is for standard division i.e divide with no remainder
                           self.height() - label1.height() // 2, 
                           label1.width(),label1.height())"""
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #HOW TO USE LAYOUT AND GRIDS IN PYQT5
        #in order to have a clean code we will define out new widget in a function
    #def initUI(self):
        """central_widget1 = QWidget()
        self.setCentralWidget(central_widget1)"""
        
        """label1 = QLabel("#1", self)
        label2 = QLabel("#2", self)
        label3 = QLabel("#3", self)
        label4 = QLabel("#4", self)
        label5 = QLabel("#5", self)
        
        #This will show us only label5 as all the other labels are placed behind it
        label1.setStyleSheet("background-color: red")
        label2.setStyleSheet("background-color: blue")
        label3.setStyleSheet("background-color: purple")
        label4.setStyleSheet("background-color: yellow")
        label5.setStyleSheet("background-color: green")
        
        #Now we will try to spread the layout vertically
        vbox = QVBoxLayout()
        
        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)
        vbox.addWidget(label4)
        vbox.addWidget(label5)
        
        #Now we will try to spread the layout horizontally
        hbox = QHBoxLayout()
        
        hbox.addWidget(label1)
        hbox.addWidget(label2)
        hbox.addWidget(label3)
        hbox.addWidget(label4)
        hbox.addWidget(label5)
        
        #Now we will try to spread the layout in a grid format
        gridbox = QGridLayout()
        
        #we have to specify the roles and columns
        gridbox.addWidget(label1, 0, 0)#i.e role 0, column 0
        gridbox.addWidget(label2, 0, 1)
        gridbox.addWidget(label3, 1, 0)
        gridbox.addWidget(label4, 1, 1)
        gridbox.addWidget(label5, 2, 2)
        
        central_widget1.setLayout(gridbox)"""
        

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #We would create an interactive button below
    """self.button.setGeometry(150, 200, 200, 100)
        self.button.setStyleSheet("font-size: 30px;")
        self.button.clicked.connect(self.on_click)
        
        self.labell.setGeometry(0, 0, 200, 100)
        self.labell.setStyleSheet("font-size: 40px;")
        
    
    #This a function that should be executed when we click a button
    def on_click(self):
        print("Button clicked")
    #to change the button on the text after being clicked
        self.button.setText("Clicked")
    #to disable the button after being clicked 
        self.button.setDisabled(True)
    #to change the text of a label when the button is clicked
        self.labell.setText("Goodbye")"""


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#We would style the checkbox under the initUI() method
    def initUI(self):
        """self.checkbox.setGeometry(10, 0, 500, 100)
        self.checkbox.setStyleSheet("font-size: 30px;"
                                    "font-family: Arial;")
        self.checkbox.setChecked(False) #so that the checked box is unchecked when the window opens
        #self.checkbox.setChecked(True) #so that the checked box is checked when the window opens
        
        self.checkbox.stateChanged.connect(self.checkbox_changed)
        
#function to be carried out when the box is checked or unchecked
    def checkbox_changed(self, state):
        if state == Qt.Checked:
            print("You like food")
        else:
            print("You do not like food")"""


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Now we will try to create radio button
        self.radio1.setGeometry(0, 0, 300, 50)
        self.radio2.setGeometry(0, 50, 300, 50)
        self.radio3.setGeometry(0, 100, 300, 50)
        self.radio4.setGeometry(0, 150, 300, 50)
        self.radio5.setGeometry(0, 200, 300, 50)
        
        #to style the radio button all at once
        self.setStyleSheet("QRadioButton{"
                           "font-size: 40px;"
                           "font-family: Arial;"
                           "padding: 10px;"
                           "}")
        
        self.button_group1.addButton(self.radio1)
        self.button_group1.addButton(self.radio2)
        self.button_group1.addButton(self.radio3)
        #group 2
        self.button_group2.addButton(self.radio4)
        self.button_group2.addButton(self.radio5)
        
    #to connect the function to the radio button
        self.radio1.toggled.connect(self.radio_button_changed)
        self.radio2.toggled.connect(self.radio_button_changed)
        self.radio3.toggled.connect(self.radio_button_changed)
        self.radio4.toggled.connect(self.radio_button_changed)
        self.radio5.toggled.connect(self.radio_button_changed)
        
    #function to be initiated when the radio button is selected
    def radio_button_changed(self):
        
    #to know and take action base on the button that was selected 
    #we will use the self.sender method to know which button
    # is the sender of the signal
        radio_button = self.sender()
        if radio_button.isChecked():
            print(f"You selected {radio_button.text()}")
        




def main():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    window = MainWindow()
    window.show() #this is to enable the window to show bcoz its default setting is to hide the window
    sys.exit(app.exec())#The "exec_()" is to enable to stay open and execute code/task till the user closes it
    

if __name__ =="__main__":
    main()