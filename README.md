# VLAN Change Utility

Menu based Python 3.x script that allows vlan changes with ease and safe guards. The tool uses DNS to authenticate via SSH to Cisco IOS switches. It provides a menu with four options to allow vlan changes.

    ("1. Show VLAN list")
    ("2. Show interface status")
    ("3. Modify interface")
    ("4. Exit")
    
The user is able to show the current vlan list, the status of all interfaces, and perform modifications to the vlan tag of those innterfaces. There are prebuilt safeguards applied to avoid misconfiguration or unintended results.

## Installation

Install netmiko library (https://pypi.org/project/netmiko/) using pip. `pip install netmiko`

## Supported Netowrking Devices

Currently tested with Cisco IOS software. The program may be modified to work with NXOS or other networking vendors. 

## Supported Python Versions

Python 3.4, 3.5, 3.6 and 3.7 are fully supported and tested. This library may work on later versions of 3, but we do not currently run tests against those versions

## Deprecated Python Versions

Python == 2.7

## How to Use

Modify the script on line 105 `'username': 'username', #Type username here!` with your user login. After activiating the program, you will be promoted to enter DNS of the device. 

`Please enter the DNS name of a device to get started e.g core1-sitecode: example.domain.com`

`The DNS and IP Address of this device is: ('example.domain.com', [], ['10.1.1.1']) `

The program will initiatie a SSH connection and request the associated password. After a successful authentication, the menu will appear. 

### Safeguards Explained
#### Invalid Port Type
If the port type does not match, error will return "invalid port type" 

    1. Show VLAN list
    2. Show interface status
    3. Modify interface
    4. Exit
    Enter your choice [1-4]: 3

    What interface would you like to modify e.g Gi0/1: 9/400

    Showing Current Configuration
    *****ERROR: INVALID PORT TYPE****

#### Restrict Port (Trunk)
If the port is a trunk, it is restricted
    What interface would you like to modify e.g Gi0/1: Te1/1

    interface TenGigabitEthernet1/1
     switchport trunk native
     switchport trunk allowed
     switchport mode trunk

    *****ERROR: RESTRICTED PORT******

#### Invalid VLAN
If the vlan does not already exist, do not allow the assignment

    Type "Yes" to change the VLAN or press any key to return: y

    Please assign VLAN number: 100
    ******ERROR: INVALID VLAN CHOICE******
