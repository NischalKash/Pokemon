import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostbyname("")

port = 9999

s.connect((host, port))

msg = s.recv(1024)
print(msg.decode('ascii'))

msg = s.recv(1024)
print(msg.decode('ascii'))

trainer2 = input()
s.send(trainer2.encode('ascii'))

faceoff_msg = s.recv(4096)
trainer1 = faceoff_msg.decode('ascii')
trainer1 = trainer1.split()
trainer1 = trainer1[-3]
print(faceoff_msg.decode('ascii'))

print("\n\n\n\n")
headline_msg = s.recv(4096)
print(headline_msg.decode('ascii'))
print("\n\n\n\n")

headline_msg = s.recv(4096)
print(headline_msg.decode('ascii'))

total_number = s.recv(4096)
total_number = total_number.decode('ascii')
total_number = int(total_number)
count = 0
print("")
while count<total_number:
    pokemon_name = s.recv(4096)
    print(pokemon_name.decode('ascii'))
    print("")
    count+=1

print("")
time.sleep(1)

for i in range(1):
    print("\n")
    pokemon_list = s.recv(4096)
    print(pokemon_list.decode('ascii'))

    headline_msg = s.recv(4096)
    print(headline_msg.decode('ascii'))

    pokemon_choosen = input()
    s.send(pokemon_choosen.encode('ascii'))

    print("\n\nPlease wait while your opponent chooses a pokemon")

data = s.recv(4096)
data = data.decode('ascii')
data = data.split('-')
print("The pokemons you have choosen is as follows")
time.sleep(0.5)
client_pokemon = data
for i in data:
    print("")
    print(i)
    time.sleep(0.5)
print("")
print("Please wait until the other player is ready")
ready = False
while ready==False:
    message = s.recv(4096)
    print(message.decode('ascii'))
    response = input()
    s.send(response.encode('ascii'))
    if response == '1':
        ready = True
        print("The battlefield is set")
print("")
print("Please wait while Trainer 1 chooses his pokemon for the battle")
choosen_client = False
count=0
while choosen_client == False:
    message = s.recv(4096)
    print(message.decode('ascii'))
    # pokemon name taken in
    response = input()
    s.send(response.encode('ascii'))
    if response in client_pokemon:
        print("The battle is as follows!!")
        messagenew = s.recv(4096)
        print(messagenew.decode('ascii'))
        status = "Alive"
        while status!="Fainted":
            attack_message = s.recv(4096)
            attack_message = attack_message.decode(('ascii'))
            attack_message = attack_message.split('-')
            status = attack_message[-1]
            if status == "Fainted":
                print("Your Pokemon has Fainted!!")
                count+=1
                if count==2:
                    print("You have lost the battle to Trainer ",trainer1,"!! But heads up!! It was Close!!")
                    choosen_client = True
                break
            if status == "OppFainted":
                print("Opponent pokemon has fainted!! Please wait while he chooses!!")
                messagenew = s.recv(4096)
                messagenew = messagenew.decode('ascii')
                if messagenew == "Win":
                    choosen_client = True
                    print("Congratulations!! You have defeated Trainer ", trainer1)
                    break
                attack_message = s.recv(4096)
                attack_message = attack_message.decode(('ascii'))
                attack_message = attack_message.split('-')
                status = attack_message[-1]
            print("The pokemon attacks are as follows !!")
            for i in attack_message:
                print(i)
                time.sleep(0.5)
            print("Choose Your Attack!!")
            attack = input()
            s.send(attack.encode('ascii'))
s.close()
