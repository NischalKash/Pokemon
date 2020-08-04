import socket
import time
import random
import xlrd

def battle(pokemon1,pokemon2,attacks,damages,health_pokemon1,health_pokemon2,server_attacks,client_attacks,superior_types,pokemon_type):
    while health_pokemon1>0 and health_pokemon2>0:
        print("The following Attacks are available with your pokemon")
        for i in attacks[pokemon1]:
            print(i)
            time.sleep(0.5)

        print("Choose the Attack you would like to order on the pokemon")
        validity_server = False
        while validity_server == False:
            attack_pokemon1 = input()
            if server_attacks[attack_pokemon1]>0:
                server_attacks[attack_pokemon1]-=1
                validity_server = True
            else:
                print("You are out of using this attack!! Please choose another one!!")

        print("Please wait while the other player chooses")
        message = '-'.join(attacks[pokemon2])
        clientsocket.send(message.encode('ascii'))
        validity_client = False
        while validity_client==False:
            attack_pokemon2 = clientsocket.recv(1024)
            attack_pokemon2 = attack_pokemon2.decode('ascii')
            if client_attacks[attack_pokemon2]>0:
                client_attacks[attack_pokemon2]-=1
                validity_client = True
                message  = "Passed"
                clientsocket.send(message.encode('ascii'))
            else:
                message = "You are out of using this attack!! Please choose another one!!"
                clientsocket.send(message.encode('ascii'))

        client_type = ""
        server_type = ""
        for i in pokemon_type:
            print(i)
            if pokemon1 in pokemon_type[i]:
                server_type = i
            if pokemon2 in pokemon_type[i]:
                client_type = i

        advantage_client = 0
        advantage_server = 0

        if client_type in superior_types[server_type]:
            advantage_server = 6
        if server_type in superior_types[server_type]:
            advantage_client = 6

        pokemon1_damage = damages[attack_pokemon1]
        pokemon2_damage = damages[attack_pokemon2]

        advantage_randomness = random.randint(0,2)
        if advantage_randomness == 2:
            pokemon2_damage = pokemon2_damage+advantage_client
            pokemon1_damage = pokemon1_damage+advantage_server

        random_variable = random.randint(0, 3)
        if random_variable == 0:
            pokemon1_damage += random.randint(1,15)
        elif random_variable == 2:
            pokemon2_damage += random.randint(1,15)

        if pokemon1_damage>pokemon2_damage:
            health_pokemon2 -= pokemon1_damage-pokemon2_damage
        else:
            health_pokemon1 -= pokemon2_damage - pokemon1_damage

        health_pokemon2-=7
        health_pokemon1-=7
        if health_pokemon1<0:
            health_pokemon1 = 0
        if health_pokemon2<0:
            health_pokemon2 = 0

        print("The health of ",pokemon1, " is ",health_pokemon1)
        print("The health of ", pokemon2, " is ", health_pokemon2)

    if health_pokemon1==0 and health_pokemon2==0:
        message = "BothFainted"
        clientsocket.send(message.encode('ascii'))
    elif health_pokemon2==0:
        message = "Fainted"
        clientsocket.send(message.encode('ascii'))
    else:
        message = "OppFainted"
        clientsocket.send(message.encode('ascii'))
    return [health_pokemon1,health_pokemon2]




serversocket = socket.socket(
	        socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"

port = 9999

serversocket.bind((host, port))

serversocket.listen(5)

print("Welcome To Pokemons Champions League!!! \nBattle of the Best!!!")

clientsocket, addr = serversocket.accept()
title_msg = "Welcome To Pokemons Champions League!!! \nBattle of the Best!!!"
clientsocket.send(title_msg.encode('ascii'))
print("Enter Trainer 1 name")
trainer1 = input()
msg = "Enter Trainer 2 Name"
clientsocket.send(msg.encode('ascii'))
trainer2 = clientsocket.recv(1024)
trainer2 = trainer2.decode('ascii')
faceoff_msg = "\n\n\n\nThe battle has been set \n"+str(trainer1)+" VS "+str(trainer2)
clientsocket.send(faceoff_msg.encode('ascii'))
print(faceoff_msg)
pokemons = []
pokemon_type = {}
loc = ("/Users/nischalkashyap/Downloads/Pokemon/pokemons.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    pokemons.append(sheet.cell_value(i, 0))
    if sheet.cell_value(i, 1) not in pokemon_type:
        pokemon_type[sheet.cell_value(i, 1)] = [sheet.cell_value(i, 0)]
    else:
        pokemon_type[sheet.cell_value(i, 1)].append(sheet.cell_value(i, 0))

superior_types = {'fire': ['grass', 'electric', 'normal', 'flying'], 'water': ['fire', 'dark', 'ground'],
                  'flying': ['water', 'ice', 'ground'], 'grass': ['water', 'normal', 'ice'],
                  'ice': ['fire', 'water', 'dark'], 'dark': ['fire', 'grass', 'normal'],
                  'electric': ['water', 'normal', 'flying'], 'ground': ['grass', 'electric', 'fire', 'normal'],
                  'normal': ['flying']}

pokemon_attacks = {}
attacks = {}
number_attacks = {}
loc = ("/Users/nischalkashyap/Downloads/Pokemon/attacks.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    attacks[sheet.cell_value(i, 0)] = sheet.cell_value(i, 1)
    number_attacks[sheet.cell_value(i,0)] = sheet.cell_value(i,3)
    attack_type = sheet.cell_value(i,2)
    attack_type = attack_type.split('/')
    for j in attack_type:
        if j in pokemon_attacks:
            pokemon_attacks[j].append(sheet.cell_value(i,0))
        else:
            pokemon_attacks[j] = [sheet.cell_value(i,0)]
new_string = ""
new2_string = ""
for i in number_attacks:
    new_string+=i+'-'
    new2_string+=str(number_attacks[i])+'-'

clientsocket.send(new_string.encode('ascii'))
time.sleep(1)
clientsocket.send(new2_string.encode('ascii'))
time.sleep(1)

print("\n\n\n\n")
headline_msg = "1. Each trainer gets to choose 5 Pokemons and will be battling with them until every pokemon is out of health \n2. Once the trainer is out of pokemons, his opponent is declared as the winner."
clientsocket.send(headline_msg.encode('ascii'))
print(headline_msg)

for j in range(2):
    time.sleep(j * 1)

print("\n\n\n\n")
headline_msg = "The following pokemons are available in the roster."
clientsocket.send(headline_msg.encode('ascii'))
print(headline_msg)

for j in range(2):
    time.sleep(j * 1)

total_number = str(len(pokemons))
clientsocket.send(total_number.encode('ascii'))

for j in range(2):
    time.sleep(j * 1)

print("")
for i in pokemons:
    print(i)
    print("")
    clientsocket.send(i.encode('ascii'))
    for j in range(2):
        time.sleep(j * 1)
time.sleep(1)

inp = random.randint(1,100000)%2
if inp==0:
    di = {trainer1:[],trainer2:[]}
else:
    di = {trainer2:[],trainer1:[]}

count = 0
while count<2:
    print("\n")
    for i in di:
        pokemon_list = "-------------------------------------------- \nThe available list of Pokemons are as follows \n --------------------------------------------"
        for j in pokemons:
            pokemon_list += "\n\n" + j

        if i==trainer2:
            clientsocket.send(pokemon_list.encode('ascii'))
            time.sleep(1)
        elif i==trainer1:
            print(pokemon_list)

        if i==trainer2:
            print("\n\nPlease wait while Trainer2 chooses a pokemon for Battle")
            headline_msg = "It is your turn to choose, please choose from the roster!! \nEnter the name of pokemon you would like to acquire!"
            clientsocket.send(headline_msg.encode('ascii'))
            pokemon_name = clientsocket.recv(1024)
            pokemon_name = pokemon_name.decode('ascii')
        else:
            print("It is your turn to choose, please choose from the roster!! \nEnter the name of pokemon you would like to acquire!")
            pokemon_name = input()

        if pokemon_name in pokemons:
            di[i].append(pokemon_name)
            pokemons.remove(pokemon_name)
            count+=1


battle_attacks = {}
health_pokemon = {}
for i in di:
    if i==trainer1:
        trainer1_pokemon = di[i]
    else:
        trainer2_pokemon = di[i]

    for j in di[i]:
        health_pokemon[j] = 100
        for k in pokemon_type:
            if j in pokemon_type[k]:
                type = k

        count = 0
        while count<4:
            attack = random.choice(pokemon_attacks[type])
            if j not in battle_attacks:
                battle_attacks[j] = [attack]
                count+=1
            else:
                if attack not in battle_attacks[j]:
                    battle_attacks[j].append(attack)
                    count+=1


for i in di:
    if i == trainer1:
        print("The pokemon you have choosen is as follows")
        time.sleep(0.5)
        for j in di[i]:
            print("")
            print(j)
            time.sleep(0.5)

    elif i == trainer2:
        data = '-'.join(di[i])
        clientsocket.send(data.encode('ascii'))
time.sleep(1)

ready_server = False
while ready_server == False:
    print("Enter 1 if you are ready to battle it out")
    a = input()
    if a=='1':
        ready_server = True
    else:
        print("Wrong Entry!! Please Enter as requested!!")

ready = False
print("Please Wait until the other player accepts your challenge!!")
while ready == False:
    message = "Trainer1 challenges you to the battlefield!! \nEnter 1 if you are ready to battle it out"
    clientsocket.send(message.encode('ascii'))
    response = clientsocket.recv(1024)
    if response.decode('ascii')=='1':
        ready = True

print("The battlefield is set")

choose_server = False
choose_client = False
while len(trainer1_pokemon)>0 and len(trainer2_pokemon)>0:
    while choose_server == False:
        print('Trainer ',trainer1," Choose Your Pokemon")
        choose_pokemon = input()
        if choose_pokemon in trainer1_pokemon:
            choose_server = True
        else:
            print("Trainer ",trainer1," Choose a pokemon you have opted")

    while choose_client == False:
        print("Please wait while the opponent chooses their Pokemon")
        message = "Trainer " + trainer2 + " Choose Your Pokemon"
        clientsocket.send(message.encode('ascii'))
        response_pokemon = clientsocket.recv(4096)
        response_pokemon = response_pokemon.decode('ascii')
        print(response_pokemon)
        if response_pokemon in trainer2_pokemon:
            choose_client = True
    print("\n")
    message = choose_pokemon+" VS "+response_pokemon
    clientsocket.send(message.encode('ascii'))
    print("The pokemon battle is as follows !!")
    print("\n")
    print(message)
    print("\n")
    server_pokemon_attacks = {}
    client_pokemon_attacks = {}
    for i in battle_attacks[choose_pokemon]:
        server_pokemon_attacks[i] = number_attacks[i]

    for i in battle_attacks[response_pokemon]:
        client_pokemon_attacks[i] = number_attacks[i]

    result = battle(choose_pokemon,response_pokemon,battle_attacks,attacks,health_pokemon[choose_pokemon],health_pokemon[response_pokemon],server_pokemon_attacks,client_pokemon_attacks,superior_types,pokemon_type)

    if result[0]==0 and result[1]==0:
        print("Both the Pokemons have fainted!!")
        trainer1_pokemon.remove(choose_pokemon)
        trainer2_pokemon.remove(response_pokemon)
        health_pokemon[choose_pokemon] = 0
        health_pokemon[response_pokemon] = 0
        choose_server = False
        choose_client = False

    elif result[0]==0:
        print("Your pokemon has fainted")
        trainer1_pokemon.remove(choose_pokemon)
        choose_server = False
        health_pokemon[choose_pokemon] = 0
        health_pokemon[response_pokemon] = result[1]
    else:
        trainer2_pokemon.remove(response_pokemon)
        choose_client = False
        health_pokemon[choose_pokemon] = result[0]
        health_pokemon[response_pokemon] = 0

time.sleep(1)
if len(trainer1_pokemon)==0 and len(trainer2_pokemon)==0:
    print("Both the Trainers are unable to battle!! This match ends in a draw!!")
    message = "Draw"
    clientsocket.send(message.encode('ascii'))
elif len(trainer1_pokemon)==0:
    print("Your pokemons are unable to continue!! Trainer ",trainer2," wins the battle")
    message = "Win"
    clientsocket.send(message.encode('ascii'))
else:
    print("Congratulations, You have won the battle against Trainer ",trainer2)

clientsocket.close()