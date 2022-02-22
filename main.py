from datetime import datetime as dt
from time import sleep
from Tracker import SQLComand,innit
innit()

def NewSection():
    print("---")
    sleep(1.2)

def Setup():
    SQLComand("""CREATE TABLE IF NOT EXISTS Accounts (
      UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      FName TEXT NOT NULL,
      Username TEXT NOT NULL,
      Pin TEXT NOT NULL,
      Phrase TEXT NOT NULL,
      LastLogin TEXT)""")


def OpeningMenu():  #The Main Menu
    opt = 0
    print("""Main Menu\n
1) Sign Up
2) Log In
3) Add Entry
4) Veiw Data
5) Sign Out
6) Quit Program""")
    while opt not in (1, 2, 3, 4, 5, 6):
        opt = input("Select: ")
        try:
            opt = int(opt)
            if opt not in (1, 2, 3, 4, 5, 6):
                print("Please enter an integer between 1 and 6.")
        except:
            print("Please enter an interger.")
    NewSection()
    return opt


def CreateAcount():
    pin1 = ""
    pin2 = ""
    username = ""
    usernames = SQLComand("""SELECT Username
               FROM Accounts""")
    print("Enter your first name.")
    name = input("Name: ")
    sleep(1.2)
    while len(username) < 5 or username in usernames:
        print("Select create a username.")
        username = input("Username:  ").lower()
        sleep(1.2)
        if len(username) < 5:
            print("Username must be 5 or more charaters.")
        elif username in usernames:
            print("Username already exists")
    while len(pin1) < 6:
        print("Please create a 6 number pin.")
        #print("Nothing important, this was made by a 16 year old on the bus so...")
        pin1 = str(input("Pin: "))
        sleep(1.2)
        if len(pin1) < 6:
            print("Pin must be atleast 6 charaters.")
    while pin1 != pin2:
        print("Re-enter your pin.")
        pin2 = str(input("Pin: "))
        sleep(1.2)
        if pin1 != pin2:
            print("Pin must mattch the first one.")
    hintPhrase = pin1
    while pin1 in hintPhrase:
        print("Create a hint phrase.")
        hintPhrase = str(input("Phrase:"))
        sleep(1.2)
        if pin1 in hintPhrase:
            print("Hint phrase cannot contain the pin")
    SQLComand(
        """INSERT INTO Accounts(FName,Username,Pin,Phrase,LastLogin)
              VALUES (:Name,:Username,:Pin,:Phrase,:Time)""", {
            "Name": name,
            "Username": username,
            "Pin": pin1,
            "Phrase": hintPhrase,
            "Time": dt.now()
        })  #CreateAcc,Add data to database
    UserId = SQLComand(
        """SELECT UserID
                       FROM Accounts
                       WHERE Username = :Username""",
        {"Username": username})[0][0]  #User ID
    print("Account Created")
    print("Logged In")
    return UserId


def LogIn():
    validUsername = False
    validPassword = False
    while validUsername == False:
        username = input("Username:  ").lower()
        sleep(1.2)
        if username == "x":
            pass  #Redirect to Report Form
        else:
            numOfUsers = SQLComand(
                """SELECT COUNT(*)
               FROM Accounts
               WHERE Username = :username""", {"username": username})[0][0]
            if numOfUsers != 1:
                print("Username doesn't exist")
                print("Enter 'x' if you've forgotton your username")
            else:
                validUsername = True
    record = SQLComand(
        """SELECT *
       FROM Accounts
       WHERE Username = :username""", {"username": username})[0]
    phrase = record[4]  #Return from Transaction
    checkedPin = record[3]  #Return from Transaction
    userID = record[0]  #Return from Transaction
    name = record[1]  #Return from Transaction
    while validPassword == False:
        inputPin = input("Pin:  ")
        sleep(1.2)
        if inputPin == "x":
            print("Hint: " + phrase)
        else:
            if inputPin != checkedPin:
                print("Incorect Pin")
                print("Enter 'x' if you've forgotton your password")
            else:
                validPassword = True
    SQLComand(
        """UPDATE Accounts
              SET LastLogin = :Time
              WHERE UserID = :ID""", {
            "Time": dt.now(),
            "ID": userID
        })
    print("Welcome " + name)
    return userID


def AddDleData():
    print("Paste the share message here:")
    dle = input()
    dle = (dle.split("\n")).remove("")
    dle[0] = dle[0].split(" ")
    if dle[0][1] == "Wordle":
        pass
        

OpeningSelection = -1
LoggedInUserID = None
print("***Welcome to Bow's DLE Tracker***")
Setup()
NewSection()
while OpeningSelection != 6:
    if LoggedInUserID == None:
        print("No User Logged In")
    else:
        print("User Logged In")
    OpeningSelection = OpeningMenu()
    if OpeningSelection == 1:
        LoggedInUserID = CreateAcount()  #Create Account
    elif OpeningSelection == 2:
        LoggedInUserID = LogIn()  #Log in
    elif OpeningSelection == 3:
        pass  #Add Dle Data
    elif OpeningSelection == 4:
        pass  #Veiw Data
    elif OpeningSelection == 5:
        pass  #Sign OUt
    if OpeningSelection != 6:
        NewSection()
print("Thank you for using Bow's DLE Tracker")
print("This program will close in:", end=" ")
for loop in range(5, 0, -1):
    print(end=str(loop))
    sleep(1)
