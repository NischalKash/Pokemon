import time
import random
import xlrd

print("Welcome To Battle Ash League")
print("Enter trainer1 name")
trainer1 = input()
print("Enter trainer2 name")
trainer2 = input()
print(trainer1," Vs ",trainer2)


pokemons = []
pokemon_type = {}
loc = ("/Users/nischalkashyap/Downloads/pokemons.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    pokemons.append(sheet.cell_value(i,0))
    if sheet.cell_value(i,1) not in pokemon_type:
        pokemon_type[sheet.cell_value(i,1)] = [sheet.cell_value(i,0)]
    else:
        pokemon_type[sheet.cell_value(i, 1)].append(sheet.cell_value(i, 0))

pokemon_attacks = {'fire':['ember','fire punch','quick attack','fire blast','rage','overheat','volcano','blazekick'],'water':['water gun','hydropump','whirlpool','megapunch'],'grass':['solarbeam','whip attack','razor leaves','poison powder'],'flying':['aerial ace','quick attack','peck','wing attack'],'ice':['ice beam','water gun','rapid ace','whirlpool'],'ground':['dig','headbutt','sand attack','sand storm'],'electric':['thundershock','thunderbolt','thunderwave','shock wave'],'dark':['hypnotec','sleep','confusion','darkmatter']}
superior_types = {'fire':['grass','electric','normal','flying'],'water':['fire','dark','ground'],'flying':['water','ice','ground'],'grass':['water','normal','ice'],'ice':['fire','water','dark'],'dark':['fire','grass','normal'],'electric':['water','normal','flying'],'ground':['grass','electric','fire','normal'],'normal':['flying']}


attacks = {}
loc = ("/Users/nischalkashyap/Downloads/attacks.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
for i in range(sheet.nrows):
    attacks[sheet.cell_value(i,0)] = sheet.cell_value(i,1)


print("The list of Pokemon will be displayed next")
print("Each trainer gets to choose 5 Pokemons and will be battling with them until every pokemon is out of health")
print("Once the trainer is out of pokemons, his opponent is declared as the winner")
cmd = input("Press C to continue")
if cmd=='C':
    print("The following list of pokemons are available and each player will be allowed to choose alternatively.")
    print("The player who chooses first will be randomly selected")
    for i in pokemons:
        #for j in range(2):
            #time.sleep(j * 1)
        print(i)
    time.sleep(1)

inp = random.randint(1,100000)%2
print(inp)
if inp==0:
    di = {trainer1:[],trainer2:[]}
else:
    di = {trainer2:[],trainer1:[]}

count = 0
while count<6:
    for i in di:
        print("Trainer Name : ",i)
        print("Enter the pokemon name you would like to choose")
        poke = input()
        if poke in pokemons:
            di[i].append(poke)
            pokemons.remove(poke)
            count+=1
        else:
            print("You lost your chance")
            print("Please enter valid name next")
        print("Remaining Pokemons in the roster are as follows")
        for i in pokemons:
            print(i)

        print("")
        print("")

print(di)
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

while len(trainer1_pokemon)>0 and len(trainer2_pokemon)>0:
    choose1 = False
    choose2 = True
    while choose1 == False:
        print("Trainer Name : ",trainer1)
        pokemon1 = input("Choose Your Pokemon")
        if pokemon1 not in trainer1_pokemon:
            choose1 = False
        else:
            choose1 = True

    while choose2 == False:
        print("Trainer Name : ",trainer2)
        pokemon2 = input("Choose Your Pokemon")
        if pokemon2 not in trainer2_pokemon:
            choose2 = False
        else:
            choose2 = True

