import socket
import time
import sys, select
from getpass import getpass
HOST = 'localhost'   # Symbolic name meaning all available interfaces
PORT = 7903 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST,PORT))

getUserInfo = False
gotusername = False
choice = ''

print 'Welcome to Bookface! Home of your space!'
while 1:
    
    if choice == '2':
        break
        
    while not getUserInfo:
        username = raw_input("Please enter your username: ")
        s.sendall(username)
        
        data = s.recv(4000)
        
        if "Please enter your password: " in data:
            password = getpass("Please enter your password:")
            s.sendall(password)
            
            
            data = s.recv(4000)
            if 'Sign-in successful!\n' in data:
                getUserInfo = True
                print data
                break
            else:
                print data
        else:
            print data
    
    x = 0
    while 1:
        
        time.sleep(1)
        data = s.recv(4000)
        
        if "1. Change Password \n2. Log out\n3. Send private message\n4. Refresh\n5. Read unread messages\n>" in data:
            
            choice = raw_input(data)
        
            s.sendall(choice)
            
            if choice == '1':

                data = s.recv(4000)
                while "Enter your password\n>" not in data:
                    print data
                    data = s.recv(4000)
                    
                password = getpass(data)
                s.send(password)
                
                data = s.recv(4000)
                
                while "Enter new password\n>" not in data:
                    print data
                    data = s.recv(4000)
                
                while "Enter new password" in data:
                    password = getpass(data)
                    s.send(password)

                #data = s.recv(4000)

                    while 'Password changed\n' in data:
                        print data
                    else:
                        print data
                else:
                    print data

            elif choice == '2':
                data = s.recv(4000)
                print data
                break
                
            elif choice == '3': #make sure here you account for bullshit from other user when they send shit over
                
                data = s.recv(4000)
                
                while "Please" not in data:
                    print data
                    data = s.recv(4000)
                    
                choice = raw_input(data)
                s.sendall(choice)
                
                data = s.recv(4000)
                
                while ("Write a private message to " not in data and "Invalid choice\n" not in data):
                    print data
                    data = s.recv(4000)
                    
                if "Invalid choice\n" in data:
                    print data
                else:
                    msg = raw_input(data)
                    s.sendall(msg)
                    #data = s.recv(4000)
                    #print data
            elif choice == '4':
                y = 0
            elif choice == '5':
                data = s.recv(4000)
                print data
        else:
            print data

