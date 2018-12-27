import socket
import threading 
import sys
import os

f=open("participant.txt","a")
a=0
b=0
c=0
d=0
f1=open("Report.txt",'a')
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
uname = input('Enter your name ::') #Taper le nom du client
ip = input('Enter IP address :: ') #Taper l'adresse de serveur
f.write(uname +'   connecté\n')
a=uname
b+=1
f.close()
s.connect((ip, port)) # connecter avec le serveur
print ("Hello", uname, "you are connected to server")

h=open("histo.txt","a")
h.write('Join   '+uname+'  Server\n')
h.close()
s.send(uname.encode('utf-8'))
clientcourant = True
def receiveMsg(sock):
    
    while clientcourant: 
       
             msg  = sock.recv(1024).decode('utf-8')# création d'un buffer de 1024 octets les messages
                                                #qu'on va recevoir sont de tel taille
             print(msg)                         # coder le message avec ascii et l'afficher en écran
        
threading.Thread(target = receiveMsg, args = (s,)).start()
d+=1
while clientcourant:
    tempMsg = input()
    msg = uname + '>>' + tempMsg   #FORME DE MESSAGE
    if 'quit' in msg:
        
        clientcourant = False
        s.send('quit'.encode('utf-8'))
        f=open("participant.txt","r")
        lines= f.readlines()
        f.close()
        f=open("participant.txt","w")
        f.write(uname +'   deconnecté\n')
        for line in lines:
            if line != (uname +'   connecté\n'):
                f.write(line)
        f.close()
        h=open("histo.txt","a")
        h.write('Quit   '+uname+'  Serv\n')
        
        
        
    else:
        
        
        s.send(msg.encode('utf-8'))
        c+=1
f1.write(str(a)+" "+str(b)+" "+str(c)+" "+str(d)+"\n" )
f1.close()
