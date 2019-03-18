# ******************************************************************
# Name:         DBnD_Client.py
# Date:         March 17, 2019
# Author:       Ardalan Ahanchi
# Description:  A simple CLI for accessing the DBnD database server.
# ******************************************************************

import os
import getpass
import requests
import json

# URL of the AWS server.
url = 'https://unthgdgw0h.execute-api.us-east-1.amazonaws.com/dev'

# A main function to display the initial information.
# ******************************************************************
def main():
    while True:
        clearScr()
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        menuChoice = getChoice(3)

        if menuChoice == 1:                                                     #Check Which menu item was chosen and act accordingly.
            loginMenu()
        elif menuChoice == 2:
            registerMenu()
        elif menuChoice == 3:
            print("Now Exiting.")
            break

# A simple menu for a new reigstration.
# ******************************************************************
def registerMenu():
    clearScr()

    #Get User information.
    print("Please Enter The Registration Information")
    printSeperator()

    name = input("Name (No Spaces): ")                                          #Get info from the user.
    dci = input("DCI Number (10 Digit Integer): ")
    pswd = input("Password (8 Character Minimum): ")

    body = {}
    body["name"] = name

    #Send a post request to the server.
    headerJson = {'Content-type': 'application/json'}
    response = requests.post(url + "/register", auth=requests.auth.HTTPBasicAuth(dci, pswd), data=json.dumps(body), headers=headerJson)
    responseJson = json.loads(response.text)

    if (int(response.status_code) > 299) or (int(response.status_code) < 200):  #Check for unsuccessful login.
        print(responseJson["msg"])
        print("Error Registering, Please Try Again.")
    else:
        print("Account Creation Successful. Logging In.")
        pressAny()
        mainMenu(dci, pswd)                                                     #Login Automagically if successful

# A menu for asking the user for dci and password and then logging in.
# ******************************************************************
def loginMenu():
    clearScr()

    #Get login information.
    print("Please Enter The login Information ")
    printSeperator()

    dci = input("DCI Number: ")
    pswd = input("Password: ")

    #Chech if the credentials are right.
    response = requests.get(url + "/player", auth=requests.auth.HTTPBasicAuth(dci, pswd))
    if (int(response.status_code) > 299) or (int(response.status_code) < 200):
        print("Error Logging in, Please Try Again.")
        pressAny()
    else:
        print("Logging In.")
        pressAny()
        mainMenu(dci, pswd)

# A main menu which asks the user what the user wants to do after login.
# *********************************************************************
def mainMenu(_dci, _pswd):
    while True:
        clearScr()
        print("Main Menu")
        printSeperator()
        print("1. List Characters")
        print("2. Add Character")
        print("3. Logout")

        menuChoice = getChoice(3)

        if menuChoice == 1:
            listCharacters(_dci, _pswd)
        elif menuChoice == 2:
            addCharacter(_dci, _pswd)
        elif menuChoice == 3:
            break
        else:
            print("Invalid Choice, Please Try Again.")

# A dialog for adding a new character.
# ******************************************************************
def addCharacter(_dci, _pswd):
    clearScr()
    print("Please Enter the new Character Information")
    printSeperator()

    #Get new character data.
    charName = input("Enter New Character Name: ")
    charRace = input("Enter New Character Race: ")
    charClass = input("Enter New Character Class: ")
    charBg = input("Enter New Character Background: ")
    charlvl = input("Enter New Character Level: ")

    #Create a json file for the server.
    body = {}
    body["race"] = charRace
    body["class"] = charClass
    body["background"] = charBg

    try:
        body["level"] = int(charlvl)
    except:
        print("Character Level must be an integer, please try again.")
        return

    #Send a post request and add the character.
    headerJson = {'Content-type': 'application/json'}
    response = requests.post(url + "/character/" + charName, auth=requests.auth.HTTPBasicAuth(_dci, _pswd), data=json.dumps(body), headers=headerJson)

    #Check the return code for errors adding the character.
    if (int(response.status_code) > 299) or (int(response.status_code) < 200):
        print("Error creating the character. Please Try Again!")
    else:
        print("Character Created.")

    pressAny()

# A menu for seeing all characters and accessing them.
# ******************************************************************
def listCharacters(_dci, _pswd):
    while True:
        clearScr()
        print("Characters List")
        printSeperator()

        #Get the list of the characters from the server.
        response = requests.get(url + "/character", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
        characters = json.loads(response.text)

        #Print all the characters.
        choiceNum = int(1)
        for character in characters["body"]:
            print(str(choiceNum) + ". Name: " + character[1] + " | Race: " + character[2] + " | Class: " + character[3] + " | Background: " + character[4] + " | Level: " + str(character[5]))
            choiceNum += 1

        if choiceNum == 1:
            print("No Characters added yet!")

        print(str(choiceNum) + ". Go Back")

        #Get the user input.
        charChoice = getChoice(choiceNum)

        #Go Back to character menu if its back.
        if(charChoice == choiceNum):
            break

        characterMenu(_dci, _pswd, characters["body"][int(charChoice) - 1])

# A function for showing the different actions for a character.
# ******************************************************************
def characterMenu(_dci, _pswd, _character):
    while True:
        clearScr()                                                              #Get the screen ready
        print("Character Menu")
        printCharacter(_character)
        printSeperator()

        print("1. View Progression")                                            #Display menu items
        print("2. View Log Sheets")
        print("3. View Downtime Log Sheets")
        print("4. View Adventure Log Sheets")
        print("5. View Magic Items")
        print("")
        print("6. Add Downtime Log Sheet")
        print("7. Add Adventure Log Sheet")
        print("8. Add Magic Item")
        print("9. Set Level")
        print("10. Go Back")

        choice = getChoice(10)                                                  #Get the user choice

        if choice == 1:
            viewProgression(_character, _dci, _pswd)                            #Call functions accordingly
        if choice == 2:
            viewAllLogSheets(_character, _dci, _pswd)
        elif choice == 3:
            viewDtLogSheets(_character, _dci, _pswd)
        elif choice == 4:
            viewAdvLogSheets(_character, _dci, _pswd)
        elif choice == 5:
            viewMagicalItems(_character, _dci, _pswd)
        elif choice == 6:
            addDtLogSheet(_character, _dci, _pswd)
        elif choice == 7:
            addAdvLogSheet(_character, _dci, _pswd)
        elif choice == 8:
            addMagicalItem(_character, _dci, _pswd)
        elif choice == 9:
            setLevel(_character, _dci, _pswd)
            _character = updateCharacter(_character, _dci, _pswd)
        elif choice == 10:
            break

# A function which gets and prints the progression info for a character.
# ******************************************************************
def viewProgression(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready
    print("Progression Information for Character")
    printCharacter(_character)
    printSeperator()

    #Get the progression info with a get character.
    response = requests.get(url + "/character/" + _character[1] + "/progression", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    prog = json.loads(response.text)

    for p in prog["progression"]:                                               #Print the progression information.
        print("Sum(Delta Downtime): " + str(p[5]))
        print("Sum(Delta TCP T1):  " + str(p[6]))
        print("Sum(Delta TCP T2):  " + str(p[7]))
        print("Sum(Delta TCP T3):  " + str(p[8]))
        print("Sum(Delta TCP T4):  " + str(p[9]))
        print("Sum(Delta Gold):  " + str(p[10]))
        print("Sum(Delta ACP):  " + str(p[11]))
        print("Sum(Delta Renown):  " + str(p[12]))

    pressAny()

# A function which gets all the logsheets and prints them accordingly.
# ******************************************************************
def viewAllLogSheets(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("All the log Sheets for Character")
    printCharacter(_character)
    printSeperator()

    #Get all the logsheets with a get request.
    response = requests.get(url + "/character/" + _character[1] + "/logs", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    sheets = json.loads(response.text)

    for sheet in sheets["logs"]:
        sheet = [str('-') if s is None else s for s in sheet]                   #Remove None values and print the sheets.
        print("")
        print("* Name: " + str(sheet[1]) + " | Adventure Name: " + str(sheet[2]) + " | Date: " + str(sheet[3]) + " | Delta Downtime: " + str(sheet[4]) + " | TCP T1: " + str(sheet[5]) + " | TCP T2: " + str(sheet[6]))
        print("  TCP T3: " + str(sheet[7]) + " | TCP T4: " + str(sheet[8]) + " | Delta Gold: " + str(sheet[9]) + " | Delta ACP: " + str(sheet[10]) + " | Delta Renown: " + str(sheet[11]) + " | DM Dci: " + str(sheet[12]) + " | Log Type: " + str(sheet[13]))

    pressAny()

# A function which gets all the downtime logsheets and prints them accordingly.
# ****************************************************************************
def viewDtLogSheets(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Downtime Log Sheets for Character")
    printCharacter(_character)
    printSeperator()

    response = requests.get(url + "/character/" + _character[1] + "/downtime_logs", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    sheets = json.loads(response.text)

    for sheet in sheets["body"]:
        sheet = [str('-') if s is None else s for s in sheet]                   #Remove None values.
        print("")
        print("* Date: " + str(sheet[3]) + " | Delta Downtime: " + str(sheet[4]) + " | Delta Gold: " + str(sheet[5]) + " | TCP T1: " + str(sheet[6]) + " | TCP T2: " + str(sheet[7]))
        print("  TCP T3: " + str(sheet[8]) + " | TCP T4: " + str(sheet[9]) + " | Delta ACP: " + str(sheet[10]) + " | Delta Renown: " + str(sheet[11]))

    pressAny()

# A function which gets all the adventure logsheets and prints them accordingly.
# ****************************************************************************
def viewAdvLogSheets(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Adventure Log Sheets for Character")
    printCharacter(_character)
    printSeperator()

    response = requests.get(url + "/character/" + _character[1] + "/adventure_logs", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    sheets = json.loads(response.text)

    for sheet in sheets["body"]:
        sheet = [str('-') if s is None else s for s in sheet]                   #Remove None values.
        print("")
        print("* Adventure Name: " + str(sheet[3]) + " | Date: " + str(sheet[4]) + " | Delta Downtime: " + str(sheet[5]) + " | TCP T1: " + str(sheet[6]) + " | TCP T2: " + str(sheet[7]))
        print("  TCP T3: " + str(sheet[8]) + " | TCP T4: " + str(sheet[9]) + " | Delta Gold: " + str(sheet[10]) + " | Delta ACP: " + str(sheet[11]) + " | Delta Renown: " + str(sheet[12]) + " | DM Dci: " + str(sheet[13]))

    pressAny()                                                                  #Wait for user input to go back.

# A function which gets all the magical items for a player and prints them.
# ****************************************************************************
def viewMagicalItems(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Magical Items for Character")
    printCharacter(_character)
    printSeperator()

    response = requests.get(url + "/magic_items/" + _character[1] , auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    items = json.loads(response.text)


    for item in items["body"]:
        item = [str('-') if i is None else i for i in item]                     #Remove None values.
        print("")
        print("* Name: " + str(item[2]) + " | Quantity: " + str(item[3]) + " | Date Acquired: " + str(item[4]))

    pressAny()

# Gets the information for a new downtime log entry and sends it to the database.
# *******************************************************************************
def addDtLogSheet(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Add new downtime log sheet for Character")
    printCharacter(_character)
    printSeperator()

    dtDate = input("Enter Date (YYYY-MM-DD): ")                                 #Get new character data.
    ddt = input("Enter Delta Downtime: ")
    tcpt1 = input("Enter TCP T1: ")
    tcpt2 = input("Enter TCP T2: ")
    tcpt3 = input("Enter TCP T3: ")
    tcpt4 = input("Enter TCP T4: ")
    dgold = input("Enter Delta Gold: ")
    dacp = input("Enter Delta ACP: ")
    drn = input("Enter Delta Renown: ")

    try:                                                                        #Create a json file for the server.
        body = {}
        body["dt_date"] = dtDate
        body["delta_downtime"] = int(ddt)
        body["delta_tcp_t1"] = int(tcpt1)
        body["delta_tcp_t2"] = int(tcpt2)
        body["delta_tcp_t3"] = int(tcpt3)
        body["delta_tcp_t4"] = int(tcpt4)
        body["delta_gold"] = int(dgold)
        body["delta_acp"] = int(dacp)
        body["delta_renown"] = int(drn)
    except:
        print("Invalid values, please try again.")
        return

    headerJson = {'Content-type': 'application/json'}                           #Send a post request and add the downtime log entry.
    response = requests.post(url + "/character/" + _character[1] + "/downtime_logs", auth=requests.auth.HTTPBasicAuth(_dci, _pswd), data=json.dumps(body), headers=headerJson)

    if (int(response.status_code) > 299) or (int(response.status_code) < 200):  #Check the return code for errors adding the character.
        print("Error. Please Try Again!")
    else:
        print("Log Added.")

    pressAny()

# Gets the information for a new adventure log entry and sends it to the database.
# ********************************************************************************
def addAdvLogSheet(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Add new Adventure log sheet for Character")
    printCharacter(_character)
    printSeperator()

    name = input("Enter Adventure Name: ")                                      #Get new character data.
    date = input("Enter Date (YYYY-MM-DD): ")
    ddt = input("Enter Delta Downtime: ")
    tcpt1 = input("Enter TCP T1: ")
    tcpt2 = input("Enter TCP T2: ")
    tcpt3 = input("Enter TCP T3: ")
    tcpt4 = input("Enter TCP T4: ")
    dgold = input("Enter Delta Gold: ")
    dacp = input("Enter Delta ACP: ")
    drn = input("Enter Delta Renown: ")
    dmdci = input("Enter the DM DCI: ")

    try:                                                                        #Create a json file for the server.
        body = {}
        body["adventure_name"] = name
        body["a_date"] = date
        body["delta_downtime"] = int(ddt)
        body["delta_tcp_t1"] = int(tcpt1)
        body["delta_tcp_t2"] = int(tcpt2)
        body["delta_tcp_t3"] = int(tcpt3)
        body["delta_tcp_t4"] = int(tcpt4)
        body["delta_gold"] = int(dgold)
        body["delta_acp"] = int(dacp)
        body["delta_renown"] = int(drn)
        body["dm_dci"] = dmdci

    except:
        print("Invalid values, please try again.")
        return

    headerJson = {'Content-type': 'application/json'}                           #Send a post request and add the adventure log.
    response = requests.post(url + "/character/" + _character[1] + "/adventure_logs", auth=requests.auth.HTTPBasicAuth(_dci, _pswd), data=json.dumps(body), headers=headerJson)


    if (int(response.status_code) > 299) or (int(response.status_code) < 200):  #Check the return code for errors adding the character.
        print("Error. Please Try Again!")
    else:
        print("Log Added.")

    pressAny()

# Gets the information for a magical item for a player and sends it to the database.
# *********************************************************************************
def addMagicalItem(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Add a new Magic Item for Character")
    printCharacter(_character)
    printSeperator()

    name = input("Enter Item Name: ")                                           #Get the item data.
    qty = input("Enter Quantity: ")
    date = input("Enter Date Aquired (YYYY-MM-DD): ")

    try:                                                                        #Create a json file for the server.
        body = {}
        body["item_name"] = name
        body["quantity"] = int(qty)
        body["date_acquired"] = date

    except:
        print("Invalid values, please try again.")
        return

    headerJson = {'Content-type': 'application/json'}                           #Send a post request and add the character.
    response = requests.post(url + "/magic_items/" + _character[1] , auth=requests.auth.HTTPBasicAuth(_dci, _pswd), data=json.dumps(body), headers=headerJson)

    if (int(response.status_code) > 299) or (int(response.status_code) < 200):  #Check the return code for errors adding the character.
        print("Error. Please Try Again!")
    else:
        print("Magical Item Added.")

    pressAny()

def setLevel(_character, _dci, _pswd):
    clearScr()                                                                  #Get the screen ready.
    print("Set new level for Character")
    printCharacter(_character)
    printSeperator()

    newLevel = input("Enter The New Level: ")                                   #Get new character data.

    body = {}                                                                   #Create a json file for the server.
    body["level"] = newLevel

    try:
        body["level"] = int(newLevel)
    except:
        print("Character Level must be an integer, please try again.")
        return

    headerJson = {'Content-type': 'application/json'}                           #Send a post request and add the character.
    response = requests.put(url + "/character/" + _character[1], auth=requests.auth.HTTPBasicAuth(_dci, _pswd), data=json.dumps(body), headers=headerJson)

    if (int(response.status_code) > 299) or (int(response.status_code) < 200):  #Check the return code for errors adding the character.
        print("Error Updating the Level. Please Try Again!")
    else:
        print("Level Updated.")

    pressAny()

#A function which gets the updated character info from the server and returns it.
# *******************************************************************************
def updateCharacter(_character, _dci, _pswd):
    response = requests.get(url + "/character", auth=requests.auth.HTTPBasicAuth(_dci, _pswd))
    characters = json.loads(response.text)                                      #Get response and convert to JSON.

    for char in characters["body"]:                                             #Update the previous character and return.
        if char[1] == _character[1]:
            _character = char

    return _character

#Print the given character in a specific format.
# ****************************************************************************
def printCharacter(_character):
    print("Name: " + _character[1] + " | Race: " + _character[2] + " | Class: " + _character[3] + " | Background: " + _character[4] + " | Level: " + str(_character[5]))

#A functin for printing a seperator.
def printSeperator():
    print("************************************\n")

#get the choice from the user and check its range.
# ****************************************************************************
def getChoice(max):
    while True:
        try:
            choice = int(input("\nEnter Choice: "))

            if choice > max:                                                    #Check if the choice size is invalid.
                raise Exception("More than the max allowed.")

            if choice < 0 or choice == 0:                                       #Raise an exception and print an error if invalid.
                raise Exception("Invalid Range.")

            return choice
        except:
            print("Invalid Choice, Please Try Again.")

#A function to pause the program until user input.
# ****************************************************************************
def pressAny():
    input("\nPress Any Key To Continue...")

#A function for clearing the screen on all operating systems (So the text doesn't move).
# **************************************************************************************
def clearScr():
    os.system('cls')        #For Windows
    os.system('clear')      #For Linux and Mac
    printLogo()

#A function for printing logos.
# ****************************************************************************
def printLogo():
    print("\n************************************\n")
    print("██████╗ ██████╗    ██╗   ██████╗ ")
    print("██╔══██╗██╔══██╗   ██║   ██╔══██╗")
    print("██║  ██║██████╔╝████████╗██║  ██║")
    print("██║  ██║██╔══██╗██╔═██╔═╝██║  ██║")
    print("██████╔╝██████╔╝██████║  ██████╔╝")
    print("╚═════╝ ╚═════╝ ╚═════╝  ╚═════╝ ")
    print("\n************************************\n")

if __name__ == '__main__':
    main()
