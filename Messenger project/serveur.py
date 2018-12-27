import socket
import threading
import os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création du socket
servercourant = True #booleen assure si le 
ip ='' #str(socket.gethostbyname(socket.gethostname())) # Prendre l'adresse ip de pc
port = 1234

clients = {}

s.bind((ip,port)) # binder le serveur avec l'adresse ip et le port
                        # le client doit connaitre ces parametres
print ('Server ready, waiting for requests ..')
s.listen() # configurer la connexion avec maximum de clients ,le serveur peut entendre simultanément

#print('Adresse ip  du serveur est:: %s'%ip)


def handleClient(client, uname):
     clientconnect = True
     keys = clients.keys()
    
     while clientconnect:
              
                   msg = client.recv(1024).decode('utf-8')
                   response = 'Nember of users connected \n'
                   found = False
                   if '**chatlist' in msg:
                       clientNo = 0
                       for name in keys:
                               clientNo += 1
                               response = response + str(clientNo) +'::' + name+'\n'
                               
                       client.send(response.encode('utf-8'))
                       
                   elif '**broadcast' in msg:
                          msg= msg.replace('**broadcast','')
                          for k,v in clients.items():
                              v.send(msg.encode('utf-8'))
                              h=open("histo.txt","a")
                              h.write('Send   '+uname+'  Tous\n')
                              h.close()
                   elif 'quit' in msg:
                          response = 'Pauser la session et exiter...'
                          client.send(response.encode('utf-8'))
                          clients.pop(uname)
                         
                          print(uname + '  is now disconnected')
                          clientconnect = False
                           
                          
                                
                   else:
                       for name in keys:
                             if('**'+name) in msg:
                                 msg= msg.replace('**'+name, '')
                                 clients.get(name).send(msg.encode('utf-8'))
                                 h=open("histo.txt","a")
                                 h.write('Send   '+uname+'  '+name+'\n')
                                 h.write('Recv   '+name+'  '+uname+'\n')
                                 h.close()
                                 found = True
                       if(not found):
                             client.send('Try to send a message to a valid person'.encode('utf-8'))
               



while servercourant: 
            client,address = s.accept() # accepter nouvelle connection ,une nouvelle socket assure la connection avec ce client spécifie
            uname = client.recv(1024).decode('utf-8')
            print('%s  has joined :: connected to server '%str(uname))
            client.send('Welcome to messenger \n1::**chatlist-> List of connected users \n2::**quit->Close the session\n3::**broadcast-> send a message to all connected users \n4::Add the name of the user at the end of your message preceded by **'.encode('utf-8')) # on encode le message avec ascii
                                                         #pour envoyer des chaines de caractéres

            if(client not in clients):
               clients[uname] = client
               threading.Thread(target = handleClient, args = (client,uname,)).start()
              
              
