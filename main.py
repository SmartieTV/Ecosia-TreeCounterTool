# Unofficial Ecosia Treecounter:
# Shows the amount of trees planted by Ecosia (www.ecosia.org)
# By SmartieTV (smartietv.de or youtube.com/smartietv)
version = ("220227.06 (Stable)")

try: #Required imports
  from bs4 import BeautifulSoup #Used for parsing html data.
  import requests #Used for requesting web page.
  from urllib.request import urlopen as uReq
  import time #Used for time delays.
  from os import system,name #Used for system-related tasks.
  import os #Also used for some system-related tasks. 
  import re #Used with bs4 to parse data.
except Exception as e1:
  print("An error occured while trying to import the necessary libraries. Error: " + str(e1))
  try: #Try to manually install/import libraries.
    print("Trying to install necessary libraries...")
    exec("sudo pip install BeautifulSoup4")
  except:
    try:
      execCmd = ("sudo apt-get install python3-bs4")
      exec(execCmd)
    except Exception as e2:
      print("Could not install necessary libraries. Error: " + str(e2))
      print("""
-> sudo pip install BeautifulSoup4
or
-> sudo apt-get install python3-bs4

Exiting program.
      """)
      exit()

#Don't change, they will be changed programatically anyway.
treeCount = 0
delay = 1.3
checkCount = 0

def clearScreen(): #Clear content on the screen.
  clearHeight = 70 #Height, which is cleared when "clear" doesn't work.
  try:
    if name == 'nt':
      _ = system('cls')
    else:
      _ = system('clear')
  except Exception as e8:
    print("\n" * clearHeight)

def cff(): #Check for mandatory files and create them if necessary.
  licensePath = ("license.txt")
  readmePath = ("readme.txt")
  licenseTxt = """MIT LICENSE
Copyright (c) 2022 SmartieTV (smartietv.de)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
  readmeTxt = """This program tracks the amount of trees planted by Ecosia, a non-profit search engine (which I encourage you to give a try). You can set a custom delay, in which the counter gets synchronized with their API (works fine when set to once every hour or day). The greater the delay, the bigger the difference between the client and the API. For debugging purposes, a log gets created & updated with every synchronization (lastScrape.txt). It tracks the time (UNIX), the result, the difference between the client and the API, the time it has been running and much more. Since the data is pulled from Ecosia's API, I can neither guarantee its accuracy, nor be held accountable for its results.
Currently working on possibilities of integrating it elsewhere, like with smart home appliances, RGB-setups, etc. 
If you have suggestions, please feel free to contact me at: info@smartietv.de."""
  if not os.path.isdir(licensePath):
    with open(licensePath ,"w") as f:
      f.write(licenseTxt)
  if not os.path.isdir(readmePath):
    with open(readmePath, "w") as f2:
      f2.write(readmeTxt)

def checkTreeCount(runTime,otc): #Function for obtaining & updating/synchronizing treecount from API with the client. 
  print("")
  print("Updating treecount from Ecosia's servers.")
  print("")
  global treeCount
  global delay
  global checkCount
  apiUrl = ("https://api.ecosia.org/v1/trees/count?utm_source=ecosiatool-V:" + str(version) + "&utm_medium=pythonprogram&utm_campaign=smrtv.de")
  response = requests.get(apiUrl)
  if response.status_code != 200:
    e3 = response.status_code
    print("An error occurred, while trying to connect to Ecosia's servers. Error: " + str(e3))
    lastScrapeTxt = ("\nLatest scrape result:\nTime (UNIX): " + str(time.time()) +"\nVersion: " + str(version) + "\nCheckCount: " + str(checkCount) + "\nRunTime: " + str(runTime) + "s\nResult: An error occurred, while trying to connect to Ecosia's servers. Error: " + str(e3) + "\n---")
    f = open("lastScrape.txt", "a")
    f.write(lastScrapeTxt)
    f.close()
    cooldownTime = 60 #Time for cooldown (in seconds)
    print("Trying again in " + str(cooldownTime) + " seconds.")
    time.sleep(cooldownTime)
    checkTreeCount(runTime,otc)
  else:
    if checkCount != 0:
      checkCount = checkCount + 1
    else:
      checkCount = 1
    content = response.content
    soup = BeautifulSoup(response.content, 'html.parser')
    txt = soup.get_text()
    treeCount = txt.replace("}","")
    treeCount = treeCount.replace(","," ")
    treeCount = treeCount.split(" ")
    for i in treeCount:
      try:
        float(i)
        if float(i) > 1000:
          treeCount = i
        else:
          delay = i
      except ValueError:
        "Not a number!"
    diffTC = int(treeCount) - int(otc) #Calculates difference between server and client.
    lastScrapeTxt = ("\nLatest scrape result:\nTime (UNIX): " + str(time.time()) +"\nVersion: " + str(version) + "\nCheckCount: " + str(checkCount) + "\nDifference (client/api): " + str(diffTC) + "\nRunTime: " + str(runTime) + "s\nResult:\n" + str(soup) + "\n---")
    f = open("lastScrape.txt", "a")
    f.write(lastScrapeTxt)
    f.close()
    printTreeCount(treeCount,delay)

def printTreeCount(treeCount,delay): #Function for printing & locally updating the current value on the screen.
  global runTime
  runTimeM = 0
  runTimeValue = "s"
  ogTreeCount = int(treeCount)
  ogTreeCountUpdate = ogTreeCount + 1400 #Default: 1400 (About 0.5 hours at 1,3spt). Rate (in trees) in which data gets synchronized with the API and gets logged to file. Important: The greater the value, the larger the difference between the local and the API value becomes. 
  treesRemainingBeforeUpdate = 1000
  timeRemaining = 0
  timeRemaingM = 0
  timeRemainingValue = "s"
  try:
    if runTime in locals():
      "NOTHING"
    else:
      "NOTHING"
  except:
    runTime = 0
  ptc = ("true")
  while ptc == ("true"): #Change the visuals of time values. 
    if timeRemaining > 60:
      timeRemainingM = timeRemaining / 60
      timeRemainingValue = "m"
    else:
      timeRemainingValue = "s"
    if runTime > 60:
      runTimeM = runTime / 60
      runTimeValue = "m"
    else:
      runTimeValue = "s"
    print("Unofficial Ecosia Treecounter")
    print("-----------------------------")
    print("TreeCount: " + str(treeCount))
    print("")
    #print("New tree every " + str(delay) + "s")
    if timeRemainingValue == "m":
      print("Synchronizing in " + str(int(timeRemainingM)) + "m")
    else:
      print("Synchronizing in " + str(int(timeRemaining)) + "s")
    if runTimeValue == "s":
      print("Running for: " + str(round(runTime,2)) + "s")
    else:
      print("Running for: " + str(round(runTimeM,1)) + "m")
    print("Version: " + str(version))
    print("\nAll results without guarantee.")
    print("Consult the readme.txt for further information.")
    treeCount = int(treeCount) + 1
    treesRemainingBeforeUpdate = ogTreeCountUpdate - int(treeCount)
    time.sleep(float(delay))
    timeRemaining = int(treesRemainingBeforeUpdate) * float(delay)
    runTime = runTime + float(delay)
    clearScreen()
    if int(treeCount) > ogTreeCountUpdate:
      ptc = ("false")
      checkTreeCount(runTime,treeCount)

def runMain(): #Start the program (loop)
  cff()
  checkTreeCount(0,0)

if __name__ == "__main__": #Checks if program is executed correctly.
  runMain()
else:
  print("Program has not been executed correctly! Run the program as main.py!")