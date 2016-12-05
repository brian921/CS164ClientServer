import socket
import time
import sys, select
from getpass import getpass
import select
import sys

class TimeoutExpired(Exception):
    pass
    
def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [],[], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n') # expect stdin to be line-buffered
    raise TimeoutExpired

HOST = '10.0.0.4'   # Symbolic name meaning all available interfaces
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
            password = getpass("Please enter your password: ")
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
        
        data = s.recv(4000)
        
        if "\n1. Change Password \n2. Log out\n3. Send private message\n4. Read unread messages\n5. View Inbox\n6. See Friends\n7. Send Friend Request\n8. View Friend Requests\n9. Post Status\na. View Your Wall\nb. View News Feed\n>" in data:
            
            try: 
                choice = input_with_timeout(data, 3)
            except TimeoutExpired:
                choice = '32'
        
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
                
                if "Enter new password" in data:
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
                
            elif choice == '3': 
                
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
                    
            elif choice == '32':
                sys.stderr.write("\x1b[2J\x1b[H")
            elif choice == '4':
                data = s.recv(4000)
                print data
                stopViewingUnread = raw_input("Press enter to continue\n")
            elif choice == '5':
                data = s.recv(4000)
                print data
                stopViewingUnread = raw_input("Press enter to continue\n")
            elif choice == '6':
                data = s.recv(4000)
                print data
                stopViewingUnread = raw_input("Press enter to continue\n")
            elif choice == '7':
                data = s.recv(4000)
                chooseNewFriend = raw_input(data)
                s.sendall(chooseNewFriend)
            elif choice == '8':
                data = s.recv(4000)
                chooseToAccept = raw_input(data)
                s.sendall(chooseToAccept)
            elif choice == '9':
                data = s.recv(4000)
                status = raw_input(data)
                s.sendall(status)
                print 'status posted\n'
            elif choice == 'a':
                data = s.recv(4000)
                print data
                stopViewingUnread = raw_input("Press enter to continue\n")
            elif choice == 'b':
                data = s.recv(4000)
                print data
                stopViewingUnread = raw_input("Press enter to continue\n")
        else:
            print data
            #time.sleep(3)
            #stopViewingUnread = raw_input("Press enter to continue\n")
            

