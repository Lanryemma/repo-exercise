"""import datetime

#if you want to install with pip in terminal
#use ".venv\Scripts\activate"

date = datetime.date(2025, 1, 2)
#to print the current date 
today = datetime.date.today()

time = datetime.time(12, 30, 0)#to print a customized
#to print the current date and time
Now = datetime.datetime.now()

#to format the way the time is printed 
#we will reassign the Now variable
Now = Now.strftime("%H:%M:%S %m-%d-%y")
#%H= hour, %M=minute, %S= seconds, %m= month,  %d= day, %y= year


print(date)
print(today)
print(time)
print(Now)

#EXERCISE 1
#we gonna see if a particular date and time is past/behind the current date and time
target_datetime = datetime.datetime(2030, 1, 2, 12, 30, 1)
current_datetime = datetime.datetime.now()

if target_datetime < current_datetime:
    print("Target date has passed")
else:
    print("Target date has NOT passed")



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#EXERCISE 2
#we are going to create an alarm clock
import time
import datetime
import pygame

def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}")
    alarm_sound = "Python Journey/Clock-effect.mp3"
    is_running = True

    while is_running:
        current_time =datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)
        time.sleep(1)#i.e its should print the current time after 1 seconds
        
        if current_time == alarm_time:
            print("WAKE UP !!")
            
            #to use the sound
            pygame.mixer.init()
            pygame.mixer.music.load(alarm_sound)
            pygame.mixer.music.play()
            
            #to enable the sound to play the full length even after current_time =alarm_time
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            
            is_running = False

if __name__ == "__main__":
    alarm_time = input("Enter the alarm time (HH:MM:SS): ")
    set_alarm(alarm_time)"""




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#multithreading = used to perform multiple tasks concurrently (multitasking)
#                 Good for I/O (input/output) bound task like reading files of fetching data from APIs
#                 Threading. Thread(target=my_function)

#first we import threading
import threading
#because we want to give each task a time interval
#we import time module
import time

def walk_dog(first, last):
    time.sleep(8)
    print(f"you walk the dog {first} {last}")

def take_out_trash():
    time.sleep(2)
    print("You take out the trash")

def get_mail():
    time.sleep(4)
    print("you go get the mail")

#to do everything gradually task by task, we will call the functions out out
#walk_dog()
take_out_trash()
get_mail()

#Now to do everything at once we would use the threading module
#Now that the threading method is running everything all at once 
#the task the takes the least time(take_out_trash()) would be completed first
chore1 = threading.Thread(target=walk_dog, args=("scooby","Doo"))#to represent arguments from functions/tasks we use "args"
chore1.start()

chore2 = threading.Thread(target=take_out_trash)
chore2.start()

chore3 = threading.Thread(target=get_mail)
chore3.start()

#in-order to allow the threaded task to finish carrying out before the next written program
#we will join the thread to appear like a singe task 
chore1.join()
chore2.join()
chore3.join()

print("All chores have been completed")