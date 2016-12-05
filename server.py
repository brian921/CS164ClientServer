import socket
import sys
import time
import datetime
from thread import *
from getpass import getpass

HOST = '10.0.0.4'   # Symbolic name meaning all available interfaces
PORT = 7903 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

clients = []    #client threads
loggedIn = []   #clients currently logged in
usernames = [ "b", "s", "m" ]  #usernames
passwords = [ "d", "h", "j" ]   #passwords

readMsgs = [ [], [], [] ]   #msgs
unreadMsgs = [ [], [], [] ] #unread msgs
friends = [ [], [], [] ] #friends
friendRequests = [ [], [], [] ] #friend requests
walls = [ [], [], [], [] ] #status walls
newsFeed = [ [], [], [] ]  
 
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
            ts = time.time()
            time.sleep(0.0010)
            menu = "\n1. Change Password \n2. Log out\n3. Send private message\n4. Read unread messages\n5. View Inbox\n6. See Friends\n7. Send Friend Request\n8. View Friend Requests\n9. Post Status\na. View Your Wall\nb. View News Feed\n>"
            
            menu = "--------------------------------------------------\n" + username + "\n--------------------------------------------------\n" + "\n" + str(len(unreadMsgs[usernames.index(username)])) + " unread message(s)\n"  + "Friend Requests: " + str(len(friendRequests[usernames.index(username)]))+ "\n" + menu
                
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
                
                try:
                    uchoice = conn.recv(4000)
                    choice = int(uchoice)
                except ValueError:
                    conn.sendall("Invalid choice\n")
                    x = 0
                    continue
                else:
                    if choice < 0 or choice > x - 1:
                        conn.sendall("Invalid choice\n")
                        x = 0
                    else:
                        msg = "Write a private message to " + str(usernames[choice]) + ":\n>"
                        conn.sendall(msg)
                        
                        umsg = conn.recv(4000)
                        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                        if usernames[choice] in loggedIn:
                            
                            readMsgs[usernames.index(usernames[choice])].append(username + ": " +umsg + " (" + st + ")\n")
                            clients[loggedIn.index(usernames[choice])].sendall("\n" + username + ": " + umsg + " (" + st +")\n")
                            
                        else:
                            unreadMsgs[usernames.index(usernames[choice])].append(username + ": " +umsg + " (" + st + ")\n")
                            
                        x = 0
                    
            elif option == '32':
                x = 0
                
            elif option == '4':
                
                listOfUMSG = "Unread Messages:\n"
                
                if len(unreadMsgs[usernames.index(username)]):
                    for i in range(len(unreadMsgs[usernames.index(username)])):
                        listOfUMSG = listOfUMSG + unreadMsgs[usernames.index(username)][i] + "\n"
                        readMsgs[usernames.index(username)].append(listOfUMSG + unreadMsgs[usernames.index(username)][i])
                    
                    del unreadMsgs[usernames.index(username)][:]
                else:
                    listOfUMSG = listOfUMSG + "none\n"
                    
                conn.sendall(listOfUMSG)
            elif option == '5':
                listOfRMSG = "Inbox\n"
                
                if len(readMsgs[usernames.index(username)]):
                    for i in range(len(readMsgs[usernames.index(username)])):
                            listOfRMSG = listOfRMSG + readMsgs[usernames.index(username)][i] + "\n"
                else:
                    listOfRMSG = listOfRMSG + "none\n"
                
                conn.sendall(listOfRMSG)
            elif option == '6':
                listOfF = "Friend List\n"
                
                if len(friends[usernames.index(username)]):
                    for i in range(len(friends[usernames.index(username)])):
                        listOfF = listOfF + friends[usernames.index(username)][i] + "\n"
                else:
                    listOfF = listOfF + "none\n"
                
                conn.sendall(listOfF)
            elif option == '7':
                msg = "Please select user to send Friend Request to.\n"
                x = 0
                for i in range(len(usernames)):
                        msg = msg + str(x) + ". " + usernames[i] + "\n"
                        x = x + 1
                msg = msg + "\n>"
                conn.sendall(msg)
                
                data = conn.recv(4000)
                
                if int(data) == usernames.index(username):
                    conn.sendall("Cannot friend yourself silly\n")
                    continue
                
                elif usernames[int(data)] in friends[usernames.index(username)]:
                    conn.sendall(usernames[int(data)] + " is already your friend\n")
                    continue
                    
                else:

                    if usernames[usernames.index(username)] not in friendRequests[int(data)]:
                        friendRequests[int(data)].append(usernames[usernames.index(username)])
                    else:
                        conn.sendall("Friend request already sent to " + usernames[int(data)])
                    
                    if usernames[int(data)] in loggedIn:
                        clients[loggedIn.index(usernames[int(data)])].sendall(username + " sent you a friend request\n")
                        
           
            elif option == '8':
                listofF = "This is a list of friend requests:\n"
                
                for i in range(len(friendRequests[usernames.index(username)])):
                    listofF = listofF + str(i) + ". " + friendRequests[usernames.index(username)][i] + "\n"
                
                if len(friendRequests[usernames.index(username)]) != 0:
                    listofF = listofF + "Choose user to add or enter '!' to continue\n>"
                else:
                    listofF = listofF + "Press enter to continue\n"
                    
                    
                conn.sendall(listofF)
                
                if len(friendRequests[usernames.index(username)]) == 0:
                    continue
                    
                data = conn.recv(4000)
                
                if data != '!':
                    
                    if int(data) >= 0 and int(data) <= len(friendRequests[usernames.index(username)]):
                        
                        friends[usernames.index(username)].append(friendRequests[usernames.index(username)][int(data)])
                        friends[usernames.index(friendRequests[usernames.index(username)][int(data)])].append(username)
                        
                        conn.sendall(friendRequests[usernames.index(username)][int(data)] + " successfully added as a friend\n")
                        
                        friendRequests[usernames.index(username)].remove(friendRequests[usernames.index(username)][int(data)])
            
            elif option == '9':
                conn.sendall("Enter a status:\n>")
                
                data = conn.recv(4000)
                
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                data = data + " " + st
                walls[usernames.index(username)].append(data)
                
                if len(friends[usernames.index(username)]) > 0:
                    for i in range (len(friends[usernames.index(username)])):
                        newsFeed[usernames.index(friends[usernames.index(username)][i])].append(username + ": " + data)
                    
                    if len(newsFeed[usernames.index(friends[usernames.index(username)][i])]) > 10:
                        newsFeed[usernames.index(friends[usernames.index(username)][i])].pop(0)
            
            elif option == 'a':
                wall = "Timeline:\n"
                for i in range(len(walls[usernames.index(username)])):
                    wall =  wall + str(i + 1) + ". " + walls[usernames.index(username)][i] + "\n\n"
                conn.sendall(wall)
            
            elif option == 'b':
                news = "Newsfeed:\n"
                for i in range(len(newsFeed[usernames.index(username)])):
                    news = news + newsFeed[usernames.index(username)][i] + "\n\n"
                conn.sendall(news)
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
