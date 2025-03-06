import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QVBoxLayout, QHBoxLayout,QPushButton
from PyQt5.QtCore import Qt,QTimer, QTime
from PyQt5.QtGui import QFont,QFontDatabase #This imports are for enabling us to work with custom/external font 

#WE ARE GOING TO MAKE A DIGITAL CLOCK
"""class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        self.Time_label= QLabel("12:00:30",self) #This is used to show the time and any other message we want to display
        self.Timer = QTimer(self)
        self.initUI()
        
        
    def initUI(self):
        self.setWindowTitle("Digital Clock")
        self.setGeometry(600, 400, 300, 100)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.Time_label)
        self.setLayout(vbox)
        
        self.Time_label.setAlignment(Qt.AlignCenter)
        self.Time_label.setStyleSheet("font-size: 150px;"
                                      "color: hsl(106, 86%, 56%);")
        self.setStyleSheet("background-color: black;")
        
        #we are going to assign the custom font
        font_id =QFontDatabase.addApplicationFont("DS-DIGIT.TTF") #we assigned our custom font to a variable
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0] #this is to pick the first font that matches the description from the data base
        my_font = QFont(font_family,150)
        self.Time_label.setFont(my_font)
        
        #To update the time after each seconds
        self.Timer.timeout.connect(self.update_time)
        self.Timer.start(1000)
        
        #we call the update_time method to show thw current time
        self.update_time()
        
    #function to request the real time and assign it to our label
    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        self.Time_label.setText(current_time)


def main():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    clock = DigitalClock()
    clock.show()
    sys.exit(app.exec_())#The "exec_()" is to enable to stay open and execute code/task till the user closes it"""
    



#_____________________________________________________________________________________________________________________________________________________________________________________________________________
#WE ARE GOING TO PROGRAM A STOP WATCH WITH PyQt5
class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time = QTime(0,0,0,0) #1st "0" represent "hour", 2nd = minute, 3rd = seconds, 4th = milliseconds
        self.time_label = QLabel("00:00:00:00",self)
        self.start_button = QPushButton("start",self)
        self.stop_button = QPushButton("stop",self)
        self.reset_button = QPushButton("reset",self)
        self.timer = QTimer(self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("My Stopwatch")
        #we want to arrange the elements vertically
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        
        self.setLayout(vbox)
        
        self.time_label.setAlignment(Qt.AlignCenter)#to align the time_label to the center of the window
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)
        
        vbox.addLayout(hbox)
        
        self.setStyleSheet("""
                        QPushButton, QLabel{
                            padding: 20px;
                            font-weight: bold;
                            font-family:calibri
                        }
                        QPushButton{
                            font-size: 50px;
                        }
                        QLabel{
                            font-size: 120px;
                            background-color: hsl(178, 73%, 85%);
                            border-radius: 15px;
                        }
                        """)
    
    #Now to give our button functionality we would connect them 
    # to their corresponding methods
        self.start_button.clicked.connect(self.Start)
        self.stop_button.clicked.connect(self.Stop)
        self.reset_button.clicked.connect(self.Reset)
        self.timer.timeout.connect(self.Update_display)
    
    def Start(self):
        self.timer.start(10)
    
    def Stop(self):
        self.timer.stop()
    
    def Reset(self):
        self.timer.stop()
        self.time = QTime(0,0,0,0)
        self.time_label.setText(self.Format_time(self.time))
        
    
    def Format_time(self,time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() //10 #we are // by 10 too covert milliseconds from 3 digits to 2
        return f"{hours:02}:{minutes:02}:{seconds:02}:{milliseconds:02}"
    
    def Update_display(self):
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.Format_time(self.time))


def main1():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    stopwatch = Stopwatch()
    stopwatch.show()
    sys.exit(app.exec_())#The "exec_()" is to enable to stay open and execute code/task till the user closes it

if __name__ =="__main__":
    #main()
    main1()
