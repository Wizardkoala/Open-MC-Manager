#!/usr/bin/env python3
# Made by Benjamin Hamilton | 2020
# For questions and concerns please email Wizardkoala31@gmail.com

### THIS IS IN ALPHA !!! ###
import os, pickle, shutil, easygui
from time import sleep

#Ovoids idiots
print("This project is NOT made by nor affiliated with Mojang.")
print("This window is a console do NOT close or input anything into this window!")
print("You can minimize this window however.")
Menu = True
debug = False

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
    Name = Name.replace(" ", "_")
    os.system("md Servers\\"+Name+"\\")
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
    MaxRam = str(int(easygui.enterbox("How many gigabytes of ram do you want to dedicate?")))
    line = "echo off\ncls\ncd Servers\\"+Name+"\njava -Xmx"+MaxRam+"G -Xms1G -jar server.jar nogui\nexit"
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
        shutil.rmtree("Servers\\"+Name+"", ignore_errors=False, onerror=handleRemoveReadonly)
def RemoveName(Name):
    Names = LoadNames()
    Names.remove(Name)

    file = open("Servers.list", 'wb')
    pickle.dump(Names, file)
    file.close()

def Remove(Name):
    Confirm = easygui.ynbox("Are you sure you want to remove: "+Name, 'Open Mc Manager')
    if Confirm:
        try:
            shutil.rmtree("Servers\\"+Name, ignore_errors=False, onerror=handleRemoveReadonly)
            RemoveName(Name)

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
def Openfiles(Name):
    os.system("start Servers\\"+Name+"")

#Starts Name
def Start(Name):
    easygui.msgbox("Type stop to shutdown the server.", "Open MC Manager")
    #Starts server
    os.system("start Servers\\"+Name+"\\Run.bat")

def Import():
    #Askes for the path of the server to import
    Path = easygui.diropenbox("Open MC Manager")
    Name = os.path.basename(os.path.normpath(Path))

    Name = Name.replace(" ", "_")
    os.system("move "+Path+" Servers\\")
    os.system("ren \"Servers\\"+Name+"\" "+Name.replace(" ", "_"))

    MaxRam = str(int(easygui.enterbox("How many gigabytes of ram do you want to dedicate?")))
    data = "echo off\ncls\ncd Servers\\"+Name+"\njava -Xmx"+MaxRam+"G -Xms1G -jar server.jar nogui\nexit"
    open("Servers\\"+Name+"\\Run.bat", 'w').write(data)

    AddName(Name)
    easygui.msgbox("Server Imported!", "Open MC Manager")

def Rename(Name):
    NewName = easygui.enterbox("What do you want the new name to be?", "Open MC Manager").replace(" ", "_")

    os.system("ren Servers\\"+Name+" "+NewName)
    print("Renamed: "+Name+" To "+NewName)

    base = open("Servers\\"+NewName+"\\Run.bat", 'r').readlines()
    Data = ""
    for line in base:
        Data += line.replace(Name, NewName)
    open("Servers\\"+NewName+"\\Run.bat", 'w').write(Data)


    RemoveName(Name)
    AddName(NewName)

try:
    debugSet = open("debug.txt", 'r').readlines()
    NameEdits = False
    debug = True
    if "AllowNameEdits" in debugSet:
        NameEdits = True
except:
    DoNothing = "Okay"
#Makes sure there is a list and it is correctly setup
try:
    LoadNames()
except:
    easygui.msgbox("This project is not made by nor affiliated with mojang!")
    easygui.msgbox("You need java to be installed to use this!\nIf you have trouble try installing a JRE.", "Open MC Manager")
    file = open("Servers.list", 'wb')
    pickle.dump([], file)
    file.close()

if debug:
    if NameEdits:
        Names = LoadNames()
        cho = easygui.buttonbox("Debug mode is not stable!", "Open MC Manager: DEBUG", ["Add", "Delete"])
        name = easygui.enterbox("", "Open MC Manager: DEBUG", Names)
        if cho == "Delete":
            RemoveName(name)
        elif cho == "Add":
            AddName(name)
        else:
            print("Failed")
    else:
        easygui.msgbox("No debug options selected!", "Open MC Manager: DEBUG")


while Menu:
    Names = LoadNames()

    NamesRemoved = []
    for name in Names:
        NamesRemoved.append(name.replace("_", " "))
    #Gives a list of options
    message = "Welcome to Open MC Manager!\nIf you are thinking, This GUI is crap... You're right. I'm not too good with GUIs, but if you are feel free to contribute on git hub or emailing Wizardkoala31@gmail.com.\nYou can also send a email with any questions or suggestions, or to just chat."
    NamesRemoved.append("Create");NamesRemoved.append("Import")
    c = str(easygui.buttonbox(message,"Open MC Manager", NamesRemoved))
    c = c.replace(" ", "_")

    if c == "Create":
        Build()
    elif c == "Import":
        Import()

    elif c in Names:
        Name = c
        c = str(easygui.buttonbox("What do you want to do with "+Name.replace("_", " ")+"?", "Open MC Manager", ["Start", "Rename", "Openfiles", "Remove", "Back"]))
        if c == "Start":
            Start(Name)
            break
        elif c == "Rename":
            Rename(Name)
        elif c == "Remove":
            Remove(Name)
        elif c == "Openfiles":
            Openfiles(Name)
        elif c == "Back":
            BeLazy = True
        elif c == "None":
            break
        else:
            easygui.msgbox("Something went wrong!", "Open MC Manager: ERROR 1")

    elif c == "None":
        break

    else:
        easygui.msgbox("Something went wrong!", "Open MC Manager: ERROR 0")
