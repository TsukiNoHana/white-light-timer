import adafruit_ds3231
import time
import wiringpi                             #import libraries

def is_it_time(store):                      #check the time
    if time.localtime()==store[0]:
        if store[0]==True:                  #find the value stored at the list's first value then implement that
            wiringpi.digitalWrite(pin,1)    #Write HIGH to pin
        elif store[0]==cycle:
            cyclical(cycle)
        elif store[0]==False:
            wiringpi.digitalWrite(pin,0)    #Write LOW to pin
        del(store[0])                       #del the first position of store if the time and store matched
    elif abs(store[0]-time.localtime())>=600:   #if you have ten minutes before the next event, print the menu
        print_menu()
    is_it_time(store)                       #run again

def cyclical(cycle):                                                    #when we want to make a repeated action we call this
    cycles=int((cycle[4]-cycle[0])/(cycle[2]+cycle[3]))                 #find how many cycles there will be from the total run time divided by a single cycle's runtime
    for i in range(cycles):
        if i==0:                                                        #the first cycle should be based on the starting state
            if cycle[0][1]=='on' or cycle[0][1]=='ON' or cycle[0][1]=='On':
                wiringpi.digitalWrite(pin,1)  #Write HIGH to pin
                time.sleep(cycle[0][2])
                wiringpi.digitalWrite(pin,0)  #Write LOW to pin
                time.sleep(cycle[0][3])
            elif cycle[0][1]=='off' or cycle[0][1]=='OFF' or cycle[0][1]=='Off':
                wiringpi.digitalWrite(pin,0)  #Write LOW to pin
                time.sleep(cycle[0][3])
                wiringpi.digitalWrite(pin,1)  #Write HIGH to pin
                time.sleep(cycle[0][2])
        else:                                                           #there after, just base it on the current state
            if wiringpi.digitalRead(pin)==1:
                wiringpi.digitalWrite(pin,0)  #Write LOW to pin
                time.sleep(cycle[0][3])
                wiringpi.digitalWrite(pin,1)  #Write HIGH to pin
                time.sleep(cycle[0][2])
            elif wiringpi.digitalRead(pin)==0:
                wiringpi.digitalWrite(pin,1)  #Write HIGH to pin
                time.sleep(cycle[0][2])
                wiringpi.digitalWrite(pin,0)  #Write LOW to pin
                time.sleep(cycle[0][3])
    del(cycle[0])                                                       #when finished delete the most recent (one just implemented) list of values
                

def print_menu(store):                                                       #print the menu and send the decision to take_action
    decision=int(input("""Please Select an Option:
1. Set time to turn off
2. Set time to turn on
3. Set time on/off increments
4. Turn on
5. Turn off
6. Print current plan
7. Delete current plan
8. Delete selected time"""))
    if abs(store[0]-time.localtime())>=600:
        take_action(store, decision)
    else:
        print("Apologies, a shift is currently taking place. Please try again in ten minutes.")
        is_it_time(store)

def take_action(store, decision):
    if decision==1:
        store=store+input("When do you want the light to turn off? [YYYY,MM,DD,HH,MM,SS]")
        store[(len(store)-1)]=False
        store.sort()
    elif decision==2:
        store=store+input("When do you want the light to turn on? [YYYY,MM,DD,HH,MM,SS]")
        store[(len(store)-1)]=True
        store.sort()
    elif decision==3:
        start_state=input("What do you want the starting state to be? (on/off)")
        if start_state=='on' or start_state=='ON' or start_state=='On':
            start=input("When do you want the light to first turn on? [YYYY,MM,DD,HH,MM,SS]")
            on_len=input("How long do you want the light to be on for in a given cycle in seconds?")
            off_len=input("How long do you want the light to be off for in a given cycle in seconds?")
            end=input("When do you want the cycles to end? [YYYY,MM,DD,HH,MM,SS]")
        elif start_state=='off' or start_state=='OFF' or start_state=='Off':
            start=input("When do you want the light to first turn off? [YYYY,MM,DD,HH,MM,SS]")
            off_len=input("How long do you want the light to be off for in a given cycle in seconds?")
            on_len=input("How long do you want the light to be on for in a given cycle in seconds?")
            end=input("When do you want the cycles to end? [YYYY,MM,DD,HH,MM,SS]")
            
        i=start+start_state+on_len+off_len+end
        cycle_list.append(i)
        cycle_list.sort()
        
        store=store+start
        store[(len(store)-1)]='cycle'
        store.sort()
    elif decision==4:
        wiringpi.digitalWrite(pin,1)  #Write HIGH to pin
    elif decision==5:
        wiringpi.digitalWrite(pin,0)  #Write LOW to pin
    elif decision==6:
        for i in range(len(store)):
            if store[i]==True:
                print("The light turns on at", store[i])
            elif store[i]==False:
                print("The light turns off at", store[i])
            elif store[i]=='cycle':
                print("The light will start cycling at", store[i])
    elif decision==7:
        confirmation=input("Are you sure you want to delete the current plan? (y/n)")

        if confirmation=='y' or confirmation=='Y':
            store=[]
    elif decision==8:
        time_to_delete=input("What is the time of the action you would like to delete? [YYYY,MM,DD,HH,MM,SS]")
        del(store[time_to_delete])
        
    is_it_time(store)
    
            
pin=1
cycle_list=[]                   #initialize variables
store=[]
wiringpi.wiringPiSetupGpio()    #setup gpio interface
wiringpi.pinMode(pin,1)         #Set GPIO pin to Output
print_menu(store)               #start running the user interface
