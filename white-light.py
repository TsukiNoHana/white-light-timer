import time
import RPi.GPIO as GPIO                           #import libraries

def cyclical(start,start_state,off_len,on_len,end):                                                    #when we want to make a repeated action we call this
    cycles=int((time.mktime(time.strptime(end,'%d %m %Y %H:%M:%S'))-time.mktime(time.strptime(start,'%d %m %Y %H:%M:%S')))/(on_len+off_len))                 #find how many cycles there will be from the total run time divided by a single cycle's runtime
    print("Will perform " + str(cycles) + " number of cycles")
    for i in range(cycles):
        if i==0:                                                        #the first cycle should be based on the starting state
            print("In first cycle")
            if start_state=='on' or start_state=='ON' or start_state=='On':
                print("Start state is on")
                GPIO.output(pin,1)  #Write HIGH to pin
                time.sleep(on_len)
                GPIO.output(pin,0)  #Write LOW to pin
                time.sleep(off_len)
            elif start_state=='off' or start_state=='OFF' or start_state=='Off':
                print("Start state is off")
                GPIO.output(pin,0)  #Write LOW to pin
                time.sleep(off_len)
                GPIO.output(pin,1)  #Write HIGH to pin
                time.sleep(on_len)
        else:                                                           #there after, just base it on the current state
            print("Completed one more cycle")
            if GPIO.input(pin)==1:
                GPIO.output(pin,0)  #Write LOW to pin
                time.sleep(off_len)
                GPIO.output(pin,1)  #Write HIGH to pin
                time.sleep(on_len)
            elif GPIO.input(pin)==0:
                GPIO.output(pin,1)  #Write HIGH to pin
                time.sleep(on_len)
                GPIO.output(pin,0)  #Write LOW to pin
                time.sleep(off_len)
    
def print_menu():                                                       #print the menu and send the decision to take_action
    decision=int(input("""Please Select an Option:
1. Set time to turn off
2. Set time to turn on
3. Set time on/off increments
4. Turn on
5. Turn off
IF EMERGENCY STOP IS REQUIRED USE CTRL + C\n"""))
    take_action(decision)

def take_action(decision):
    if decision==1:
        action_time=input("When do you want the light to turn off? DD MM YYYY HH:MM:SS\n")
        while time.time()<time.mktime(time.strptime(action_time,'%d %m %Y %H:%M:%S')):
            time.sleep(0.5)
        GPIO.output(pin,0)
    elif decision==2:
        action_time=input("When do you want the light to turn on? DD MM YYYY HH:MM:SS\n")
        while time.time()<time.mktime(time.strptime(action_time,'%d %m %Y %H:%M:%S')):
            time.sleep(0.5)
        GPIO.output(pin,1)
    elif decision==3:
        start_state=input("What do you want the starting state to be? (on/off)\n")
        start=input("When do you want the cycles to start? DD MM YYYY HH:MM:SS\n")
        off_len=float(input("How long do you want the light to be off for in a given cycle in seconds?\n"))
        on_len=float(input("How long do you want the light to be on for in a given cycle in seconds?\n"))
        end=input("When do you want the cycles to end? DD MM YYYY HH:MM:SS\n")
        while time.time()<time.mktime(time.strptime(start,'%d %m %Y %H:%M:%S')):
            time.sleep(0.5)
        print("started cycling")
        cyclical(start,start_state,off_len,on_len,end)
    elif decision==4:
        GPIO.output(pin,1)  #Write HIGH to pin
    elif decision==5:
        GPIO.output(pin,0)  #Write LOW to pin

    print_menu()

pin=40
GPIO.setmode(GPIO.BCM)      #setup pin interface
GPIO.setup(pin, GPIO.OUT)   #Set GPIO pin to Output
print_menu()                #start running the user interface
