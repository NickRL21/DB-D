# A random data generator for the DBnD database.
# CSS 475
# Team DBnD
# Ardalan Ahanchi
# March 8, 2019

import random
import sys

dci_numbers = ["9368051467", "1435449448","8237504628","0218987292","5693598871","8802168279","4268512139","1257505344","5027822952","7743925518","4767023114","1722423813","0572757589","2988831439","7822167623","1517560197","0054130645","7487826575","4166839611","6670056959"]

player_names = ["Pamela", "Angela", "Louis", "Sara", "Phillip", "Margaret", "Christina", "Victor", "Ryan", "Nicole", "Lori", "Peter", "Alice", "Jonathan", "George", "Alan", "Theresa", "Phyllis", "Nicholas", "Paul"]

classes = ["Barberian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]

races = ["Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human", "Tiefling"]

backgrounds = ["Acolyte", "Charlatan", "Criminal", "Entertainer", "Folk Hero", "Gladiator", "Guild Merchant", "Hermit", "Knight", "Noble", "Outlander", "Pirate", "Sage", "Sailor", "Soldier", "Urchin"]

magical_items = ["Bag of Holding", "Bag of Tricks", "Boots of Elvenkind", "Boots of the Winterlands", "Bracers of Archery", "Brooch of Shielding", "Broom of Flying", "Cloak of Protection", "Cloak of the Manta Ray", "Deck of Illusions", "Eversmoking Bottle", "Eyes of Charming", "Eyes of Minute Seeing", "Eyes of the Eagle", "Gem of Brightness", "Goggles of Night", "Hat of Disguise", "Helm of Telepathy", "Immovable Rod", "Necklace of Adaptation", "Oil of Slipperiness", "Restorative Ointment", "Ring of Jumping", "Ring of Mind Shielding", "Wand of Web", "Wand of the War Mage", "Wind Fan", "Winged Boots"]

character_names = ["Ilona", "Lianne", "Kallie", "Melina", "Lashaun", "Donnette", "Ilene", "Kandice", "Alphonse", "Christoper", "Shane", "Jamar", "Jinny", "Daisey", "Vasiliki", "Joette", "Chelsey", "Eugene", "Deidra", "Cristin", "Kyle", "Cherly", "Shantelle", "Johnsie", "Rory", "Karlene", "Ernestina", "Henriette", "Denita", "Kasey", "Tommye", "Yuonne", "Retta", "Gricelda", "Waylon", "Chae", "Bettina", "Tammera", "Hermine", "Caitlin", "Coretta", "Elton", "Shellie", "Lynnette", "Annabelle", "Edwardo", "Demarcus", "Pattie", "Aretha", "Debrah", "Malinda", "Marget", "Winona", "Dottie", "Kazuko", "Larhonda", "Armanda", "Elfreda"]

adventure_names = ["The Dying Pirate Trade", "Outlaw of the Careless Grove", "Across Bane's Marshes", "Ioun's Murderous Traveler", "The Sorrow of Ioun", "Within Torog's Catacombs", "The Elf Within the Manor", "Before the Stream", "The Fiery Power of Nentir River", "Torog's Warlock", "The Lance of Hammerfast", "The Ailing Adventurer Wand", "The Fury of Orcus", "The Orc Above the Village", "The Sacred Marksman Doom", "The Bandit Below the Market", "Follower of the Outpost", "Through the Jail", "The Son of Corellon", "Queen of the Last Time", "Demonspawn of the Hills", "The Wealthy Head of Nentir Vale", "The Wand of Pelor", "Within Corellon's Hills", "Within Bahamut's Cell", "The Fiery Story from Above", "Orcus's Proud Sorcerer", "Corellon's Merchant", "The Servant Below the Powerful Alley", "The Menacing Conspiracy of Sigil"]

def randLogId():
    return str(random.randint(0, 50000))

def randDelta():
    return str(random.randint(1, 10))

def randLevel():
    return str(random.randint(0, 20))

def randQty():
    return str(random.randint(1, 3))

def randADowntime():
    return str(random.randint(1, 30))

def randATcp():
    return str(random.randint(1, 20))

def randAGold():
    return str(random.randint(1, 2000))

def randAAcp():
    return str(random.randint(1, 10))

def randARenown():
    return str(random.randint(1, 5))

def randDDowntime():
    return str(random.randint(-5, 5))

def randDTcp():
    return str(random.randint(-20, 20))

def randDGold():
    return str(random.randint(-1000, 2000))

def randDAcp():
    return str(random.randint(1, 10))

def randDRenown():
    return str(random.randint(-1, 5))

def randDate():
    randDate = ""
    randDate += str(random.randint(2008, 2018))
    randDate += "-"
    randDate += str(random.randint(1, 12))
    randDate += "-"
    randDate += str(random.randint(1, 28))
    return randDate

def printPlayers():
    for i in range(0, len(dci_numbers)):
        print("insert into PLAYER values (", end = "")
        print("\'" + dci_numbers[i] + "\', " , end = "")
        print("\'" + player_names[i] + "\'" , end = "")
        print(");")

def printCharacters(count):
    for i in range(count):
        randI = random.randint(0, len(dci_numbers))
        print("insert into P_CHARACTER values (", end = "")
        print("\'" + dci_numbers[randI] + "\', " , end = "")
        print("\'" + random.choice(character_names) + "\', " , end = "")
        print("\'" + random.choice(races) + "\', " , end = "")
        print("\'" + random.choice(classes) + "\', " , end = "")
        print("\'" + random.choice(backgrounds) + "\', " , end = "")
        print(randLevel() , end = "")
        print(");")

def printMagicalItems(count):
    for i in range(count):
        print("insert into MAGICAL_ITEM values (", end = "")
        print("\'" + random.choice(dci_numbers) + "\', " , end = "")
        print("\'" + random.choice(character_names) + "\', " , end = "")
        print("\'" + random.choice(magical_items) + "\', " , end = "")
        print(randQty() + ", " , end = "")
        print("\'" + randDate() + "\'" , end = "")
        print(");")

def printDTLog(count):
    for i in range(count):
        print("insert into DOWNTIME_LOG_ENTRY values (", end = "")
        print(randLogId() + ", " , end = "")
        print("\'" + random.choice(dci_numbers) + "\', " , end = "")
        print("\'" + random.choice(character_names) + "\', " , end = "")
        print("\'" + randDate() + "\', " , end = "")
        print(randDDowntime() + ", " , end = "")
        print(randDGold() + ", " , end = "")
        print(randDTcp() + ", " , end = "")
        print(randDTcp() + ", " , end = "")
        print(randDTcp() + ", " , end = "")
        print(randDTcp() + ", " , end = "")
        print(randDAcp() + ", " , end = "")
        print(randDRenown(), end = "")
        print(");")

def printADLog(count):
    for i in range(count):
        print("insert into ADVENTURE_LOG_ENTRY values (", end = "")
        print(randLogId() + ", " , end = "")
        print("\'" + random.choice(dci_numbers) + "\', " , end = "")
        print("\'" + random.choice(character_names) + "\', " , end = "")
        print("\'" + random.choice(adventure_names) + "\', " , end = "")
        print("\'" + randDate() + "\', " , end = "")
        print(randADowntime() + ", " , end = "")
        print(randATcp() + ", " , end = "")
        print(randATcp() + ", " , end = "")
        print(randATcp() + ", " , end = "")
        print(randATcp() + ", " , end = "")
        print(randAGold() + ", " , end = "")
        print(randAAcp() + ", " , end = "")
        print(randARenown(), end = "")
        print(");")


#Get the number of repetitions from the parameters and print data.
number = int(sys.argv[1])

printPlayers()
printCharacters(number)
printMagicalItems(number)
printDTLog(number)
printADLog(number)
