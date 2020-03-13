#!/usr/bin/env python3
#This file is to download a jar file while a window is still open in OpenMCManager

import requests, os

data = (open("jardownload.download", 'r').readlines())
url = data[0].replace("\n", '')
Name = data[1]

print("""This loading screen window will eventualy be improved.
We are currently downloading the jar file for the version you selected
Please wait...""")

download = requests.get(url, allow_redirects=True)
open('Servers\\'+Name+'\\server.jar', 'wb').write(download.content)

os.remove("jardownload.download")
