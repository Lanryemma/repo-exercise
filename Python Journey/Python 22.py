#Api key(a0d5c4228e89fdfe80615d32d9b13608)
#We are going to create a weather app
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit,
                            QPushButton,QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel("",self)
        self.initUI()
    
    def initUI(self):
        #To change the tittle of the window
        self.setWindowTitle("My Weather App")
        #To align the components vertically
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        #To align components to the center of the widget
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        #To give the components String names tha we can style with
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        #Now we will style th components
        self.setStyleSheet("""
                        QLabel,QPushButton{
                            font-family: calibri;
                        }
                        QLabel#city_label{
                            font-size:40px;
                            font-style:italic
                        }
                        QLineEdit#city_input{
                            font-size:40px;
                        }
                        QPushButton#get_weather_button{
                            font-size: 30px;
                            font-weight: bold;
                        }
                        QLabel#temperature_label{
                            font-size: 75px
                        }
                        QLabel#emoji_label{
                            font-size: 100px;
                            font-family: Segoe UI emoji;
                        }
                        QLabel#description_label{
                            font-size: 100px;
                        }
                        """)

        self.get_weather_button.clicked.connect(self.get_Weather)
    def get_Weather(self):
        APi_key = "a0d5c4228e89fdfe80615d32d9b13608"
        City = self.city_input.text()
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={City}&appid={APi_key}"
        
        try:
            response = requests.get(URL)
            response.raise_for_status()#The try block doesn't catch "request type errors so we have to use"raise_for_status()" to enable it to check for request status
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:#This is to catch errors when cod is 400 and above(e.g requesting data that doesn't exist)
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden \nAccess Denied")
                case 404:
                    self.display_error("Not found\ncity not found")
                case 500:
                    self.display_error("internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nInvalid response from server")
                case 503:
                    self.display_error("Service Unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred\n {http_error}")
        except requests.exceptions.ConnectionError:#incase the internet is put off
            self.display_error("Connection Error \n check your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\n The request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects\n Check the Url")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error\n{req_error}")
    
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        #when showing error there should be no emoji showing
        self.emoji_label.clear()
        #when showing error there should be no description showing
        self.description_label.clear()
    
    def display_weather(self,data):
        #Since the temperature remains at 30px after displaying the 
        # error message, have to adjust it back when we want to display the weather
        self.temperature_label.setStyleSheet("font-size: 75px")
        print(data)
        #after printing our data we can see will look for "main",which is a dictionary that contains most of the information
        # we need e.g(temperature, weather condition e.t.c)
        temperature_kel = data["main"]["temp"] #main is the dictionary and "temp" is the key to get the value of temperature
        #since the temp is in kelvin by default we will convert it to celsius and fahrenheit 
        temperature_cel = temperature_kel- 273.15
        temperature_fah = (temperature_kel * 9/5) - 459.67
        #Now we get the "weather description from the data which is a dictionary inside 
        # a list [{}] name "weather"
        weather_description = data["weather"][0]["description"]
        #Now we get the "weather id from the data which is a dictionary inside 
        # a list [{}] name "weather"
        weather_id = data["weather"][0]["id"]
        print(weather_id)
        
        self.temperature_label.setText(f"{temperature_cel:.0f}°C")
        self.description_label.setText(weather_description)
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        
    def get_weather_emoji(self,weather_id):
        if weather_id >= 200 and weather_id <= 232:
            return "⛈"
        elif 300<= weather_id <= 321: # same as (if weather_id >= 300 and weather_id <= 321)
            return "🌥"
        elif 500<= weather_id <=531:
            return "🌧"
        elif 600 <= weather_id <=622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return"🌫"
        elif weather_id ==762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return"☁"
        else:
            return ""

def main():
    app = QApplication(sys.argv)#this allows PyQt5 process any command line arguments intended for it
    Weather_app = WeatherApp()
    Weather_app.show()
    sys.exit(app.exec_())#The "exec_()" is to enable to stay open and execute code/task till the user closes it

if __name__ =="__main__":
    #main()
    main()
