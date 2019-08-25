#!/usr/bin/env python3

# Documentation...
# python -m pip install netmiko
# https://docs.python.org/2/library/socket.html
# https://docs.python.org/2/library/getpass.html

from __future__ import print_function, unicode_literals

##########################
# Import 
##########################

# Netmiko is the same as ConnectHandler
from netmiko import Netmiko
from getpass import getpass

import socket

##########################
# Functions Defintions Start
##########################

# Menu defintions 
def ciscoMenu():     
    print ("1. Show VLAN list")
    print ("2. Show interface status")
    print ("3. Modify interface")
    print ("4. Exit")

def showVlan():
    showVlan = net_connect.send_command('\nshow vlan brief') 
    print (showVlan)

def showInt():
    showInt = net_connect.send_command('\nshow int status')
    print (showInt)

# def modifyInterface():

def exitProgram():
    print ("\nExiting Program")
    print ('\nThank you for using the VLAN Change Utility, Goodbye!')
    loop=False  # Exit menu to exit application
    net_connect.disconnect()

##########################
# Functions Defintions End
##########################

print ('Welcome to the VLAN change utility.')

while True:
    # Determines which device to log into
    deviceName = input('\nPlease enter the DNS name of a device to get started e.g core1-sitecode: ')
    try:
        # Resolves DNS
        data = socket.gethostbyname_ex(deviceName)
        print ('\nThe DNS and IP Address of this device is: '+repr(data))
        break
        # Error checks for valid DNS record
    except socket.gaierror:
        print ('\nUnable to resolve hostname. Please try again.')
        #continue
print ('\nLogging in now...')

# SSH Login Details
while True:
    try:
        myDevice = {
        'host': deviceName,
        'username': 'username', #Type username here! 
        'password': getpass(),
        'device_type': 'cisco_ios',
        }
# Connects to "myDevice"
        net_connect = Netmiko(**myDevice)
        net_connect.enable()
        break
    except:
        print ('\nLogin failed. Please try again.')
        continue

while True:     # While loop which will keep going until loop = False
    ciscoMenu() # Displays menu
    menuChoice = input("Enter your choice [1-4]: ")
    if menuChoice=='1':
        showVlan()
    elif menuChoice=='2':
        showInt()
    elif menuChoice=='3':
        showInt = net_connect.send_command('\nshow int status')
        interface = input ('\nWhat interface would you like to modify e.g Gi0/1: ')
        print ('\nShowing Current Configuration')
        output = net_connect.send_command('show run int '+interface)
        if 'Invalid input detected' in output: # Checks for valid port selection 
            print ('*****ERROR: INVALID PORT TYPE****')
            continue
        print (output)
        if "switchport mode trunk" in output: # Checks for trunk port
            print ('*****ERROR: RESTRICTED PORT******')
            continue
        
        changeDecision = input('\nType "Yes" to change the VLAN or press any key to return: ').upper()
        
# Starting VLAN configuration
        if changeDecision == 'YES' or changeDecision == 'Y':
            vlanNumber = input ('\nPlease assign VLAN number: ') # User enters VLAN number
            showVlan = net_connect.send_command('\nshow vlan brief') # Store variable if user does not execute menu option1
            if vlanNumber in showVlan: # Checks for valid vlan
                print ('\nAssiging VLAN number...')
                config_commands = [                                  # config_commands list array.
                'Interface '+interface,
                'switchport access vlan '+vlanNumber 
                            ]
                net_connect.send_config_set(config_commands)
                print ('\nVlan Updated...')
                print ('\nShowing Updated Configuration')
                output = net_connect.send_command('show run int '+interface) # Show Updated Config after changes 
                print (output)
                print ('\nWriting Configuration...')
                net_connect.send_command_expect('write mem') # Write Mem
            else:
                print ('******ERROR: INVALID VLAN CHOICE******')
                continue
# Ending VLAN configuration
    elif menuChoice=='4':
        exitProgram()
        break
    else:
        # Any integer inputs other than values 1-4 print an error message
        print("\nInvalid option. Enter any key to try again..")
