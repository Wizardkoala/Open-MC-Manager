#!/usr/bin/env python3
# Made by Benjamin Hamilton | 2020
# For questions and concerns please email Wizardkoala31@gmail.com
# Made with Atom

### THIS IS IN ALPHA !!! ###
import os, pickle, shutil, easygui
from time import sleep

#Ovoids idiots
print("This project is NOT made by nor affiliated with Mojang.")
print("This window is a console do NOT close or input anything into this window!")
print("You can minimize this window however.")
Menu = True


#Load the list of known built servers
def LoadNames():
    file = open("Servers.list", 'rb')
    Names = pickle.load(file)
    file.close()
    return Names

## Copyed and slightly edited from ThomasH on stackoverflow.com
def handleRemoveReadonly(func, path, exc):
  import errno, stat
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise
## End of copy

#Adds a name to the list of known built servers
def AddName(Name):
    Names = LoadNames()

    Names.append(Name)

    file = open("Servers.list", 'wb')
    pickle.dump(Names, file)
    file.close()

#Creates a new server
def Build():
    #Needed later
    import requests
    print("If you have problems try installing a JRE before useing")
    #Creates Dir and adds to Name list
    Name = easygui.enterbox("Name the server!")
    os.system("md \"Servers\\"+Name+"\\\"")
    AddName(Name)

    #Loads the versions in names format eg. 1.15.2
    file = open("VersionsName.pkl", 'rb')
    VersionsName = pickle.load(file)
    file.close()

    #Loads versions in link format eg.
    #https://launcher.mojang.com/v1/objects/952438ac4e01b4d115c5fc38f891710c4941df29/server.jar
    file = open("VersionsLink.pkl", 'rb')
    VersionsLink = pickle.load(file)
    file.close()


    #Asks what versions you want
    Version = str(easygui.choicebox("Which Version do you want?", 'Open MC Manager', VersionsName))

    #Finds the link to the verisons you picked
    url = VersionsLink[VersionsName.index(Version)]

    #Downloads the jar file
    easygui.msgbox("This window will close and the jar file and download in the background, please wait! ", 'Open MC Manager')
    print("Downloading...")
    download = requests.get(url, allow_redirects=True)
    open('Servers\\'+Name+'\\server.jar', 'wb').write(download.content)

    #Writes the run.bat file to start the server
    MaxRam = str(int(easygui.enterbox("How much ram do you want to dedicate?")))
    line = "echo off\ncls\ncd Servers\\"+Name+"\njava -Xmx"+MaxRam+"M -Xms1024M -jar server.jar nogui\nexit"
    file = open("Servers\\"+Name+"\\Run.bat", 'w')
    file.write(line)
    file.close()

    #Preforms first time startup to generate needed ELUA and properties files
    os.system("start Servers\\"+Name+"\\Run.bat /MIN")

    sleep(3)
    EULA = str(easygui.ynbox("By inputing TRUE you are indicating your agreement to Mojang's EULA (https://account.mojang.com/documents/minecraft_eula)."))

    #Corrects ELUA file
    if EULA.lower() == "true":
        E = ''.join(open("Servers\\"+Name+"\\eula.txt", 'r').readlines())
        E = E.replace("false", "true")
        open("Servers\\"+Name+"\\eula.txt", 'w').write(E)
    else:
        print("Stopping Build")
        shutil.rmtree("Servers\\"+Name, ignore_errors=False, onerror=handleRemoveReadonly)

def Remove():
    Name = easygui.buttonbox("Which sever do you want to remove?", 'Open MC Manager', LoadNames())
    Confirm = easygui.ynbox("Are you sure you want to remove "+Name, 'Open Mc Manager')
    if Confirm:
        try:
            shutil.rmtree("Servers\\"+Name, ignore_errors=False, onerror=handleRemoveReadonly)

            Names = LoadNames()
            Names.remove(Name)

            file = open("Servers.list", 'wb')
            pickle.dump(Names, file)
            file.close()
        except:
            Names = LoadNames()
            Names.remove(Name)

            file = open("Servers.list", 'wb')
            pickle.dump(Names, file)
            file.close()
        easygui.msgbox("Server Deleted!")
    else:
        easygui.msgbox("Aborted!")


#Open the dir of Name for changes that cant be made in the manager
def Openfiles():

    d = easygui.buttonbox("Which server?", 'Open MC Manager', LoadNames())
    os.system("start Servers\\"+d)

#Starts name
def Start():
    #Checks if there is a server to start.
    if LoadNames() == []:
        easygui.msgbox("Please create a server first!", "Open MC Manager")
        sleep(2)
        return False
    else:
        Name = easygui.buttonbox("Pick a server to start", "Open MC Manager",LoadNames())
        easygui.msgbox("Type \"stop\" to shutdown the server.", "Open MC Manager")
        #Starts server
        os.system("start Servers\\"+Name+"\\Run.bat")
        return True

#Makes sure there is a list and it is correctly setup
try:
    LoadNames()
except:
    file = open("Servers.list", 'wb')
    pickle.dump([], file)
    file.close()


while Menu:
    #Gives a list of options
    message = "Welcome to Open MC Manager!\nIf you are thinking, \"This GUI is crap...\" You're right. I'm not too good with GUIs, but if you are feel free to contribute on git hub or emailing Wizardkoala31@gmail.com.\nYou can also send a email with any questions or suggestions, or to just chat."
    c = str(easygui.buttonbox(message,"Open MC Manager", ['Start', 'Openfiles', 'Create', 'Remove', 'Import'])).lower()
    if c == "start":
        if Start():
            break
    elif c == "openfiles":
        Openfiles()
    elif c == "create":
        Build()
    elif c == "import":
        easygui.msgbox("This feature is currently not avalible, sorry.")
    elif c == "remove":
        Remove()
    elif c == "none":
        break
    else:
        easygui.msgbox("Something went wrong!", "Open MC Manager: ERROR 0")
