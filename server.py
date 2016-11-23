import socket
import sys
import time
from thread import *
from getpass import getpass
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 7903 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []    #client threads
loggedIn = []   #clients currently logged in
usernames = [ "bnguy032", "steelsamurai", "mahboi21" ]  #usernames
passwords = [ "dood", "hello", "jman21" ]   #passwords

readMsgs = [ [], [], [] ]   #msgs
unreadMsgs = [ [], [], [] ] #unread msgs

print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    gotPass = False
    gotUName = False
    option = '0'
    username = ''
    #infinite loop so that function do not terminate and thread do not end.
    
    while True:
        
        if option == '2':
            break
            
        while not gotPass:
            data = conn.recv(4000)
            if data in usernames:
                username = data
                
                conn.sendall("Changing password .Please enter your password: ")
                password = conn.recv(4000)
            else:
                conn.sendall('Username not found\n')
                continue
        
            if password in passwords:
                if usernames.index(username) == passwords.index(password):
                    gotPass = True
                    conn.sendall('Sign-in successful!\n')
                else:
                    conn.sendall("Incorrect password\n")
                    continue
            else:
                conn.sendall("Incorrect password\n")
                continue
        
        loggedIn.append(username)
        
        #print data
        
        
        while 1:  
            time.sleep(1)
            menu = "1. Change Password \n2. Log out\n3. Send private message\n4. Refresh\n5. Read unread messages\n>"
            
            menu = str(len(unreadMsgs[usernames.index(username)])) + " unread message(s)\n" + menu
                
            conn.sendall(menu)
            option = conn.recv(4000)
            
            if option == '1':
                conn.sendall("Enter your password\n>")
                pdata = conn.recv(4000)
                
                if pdata in passwords:
                    if usernames.index(username) == passwords.index(pdata):
                        conn.sendall("Enter new password\n>")
                        
                        npass = conn.recv(4000)
                        
                        if npass != "":
                            passwords[passwords.index(pdata)] = npass
                            conn.sendall("Password changed.\n")
                        else:
                            conn.sendall("Password cannot be blank\n")
                    else:
                        conn.sendall("Incorrect password\n")
                        continue
                else:
                    conn.sendall("Incorrect password\n")
                    continue
                        
                        
                
            elif option == '2':
                conn.sendall("Logging out...")
                loggedIn.remove(username)   #remove user from list of users who are logged in
                clients.remove(conn)
                conn.close()
                break
                
            elif option == '3':
                msg = "Please select user to send private message to.\n"
                x = 0
                for i in range(len(usernames)):
                        msg = msg + str(x) + ". " + usernames[i] + "\n"
                        x = x + 1
                msg = msg + "\n>"
                conn.sendall(msg)
                
                uchoice = conn.recv(4000)
                
                if not uchoice == int:
                    conn.sendall("Invalid choice\n")
                    x = 0
                    continue
                    
                if int(uchoice) < 0 or int(uchoice) > x - 1:
                    conn.sendall("Invalid choice\n")
                    x = 0
                else:
                    msg = "Write a private message to " + str(usernames[int(uchoice)]) + ":\n"
                    conn.sendall(msg)
                    
                    umsg = conn.recv(4000)
                    
                    if usernames[int(uchoice)] in loggedIn:
                        readMsgs[usernames.index(usernames[int(uchoice)])].append(umsg)
                        clients[loggedIn.index(usernames[int(uchoice)])].sendall(username + ": " + umsg + "\n")
                        print uchoice
                    else:
                        unreadMsgs[usernames.index(usernames[int(uchoice)])].append(username + ": " +umsg + "\n")
                    
                    #conn.sendall("Messaged received\n")
                    #continue here do something when user is logged in/logged out
                    x = 0
            elif option == '4':
                print 'refreshed'
            elif option == '5':
                #conn.sendall("Insert unread messages here\n")
                listOfUMSG = "Unread Messages:\n"
                
                if len(unreadMsgs[usernames.index(username)]):
                    for i in range(len(unreadMsgs[usernames.index(username)])):
                        listOfUMSG = listOfUMSG + unreadMsgs[usernames.index(username)][i] + "\n"
                        readMsgs[usernames.index(username)].append(listOfUMSG + unreadMsgs[usernames.index(username)][i])
                    
                    del unreadMsgs[usernames.index(username)][:]
                else:
                    listOfUMSG = listOfUMSG + "none\n"
                conn.sendall(listOfUMSG)
                
            else:
                conn.sendall("Invalid Option.\n")
                
        if not data: 
            break
     
        #conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    
    clients.append(conn)
    
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
