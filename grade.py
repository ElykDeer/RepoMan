#!/usr/bin/env python3

################################################################################
from subprocess import call
import json
import requests
from datetime import datetime, timedelta
import ProjectSnapShots

xxx = input("Remember to give me arguments, and give me key: ")
orgname = ""

#Global time for running the script
st = datetime.now().strftime('%Y-%m-%d')
gitHubgrades = {}

#Get all repo commit within the past week and the week before, return the sha of this week and sha of week before in a string
def getSHA(repo):
    days = 14
    now = datetime.now().strftime('%Y-%m-%d')
    week_before = (datetime.now() - timedelta(days)).strftime('%Y-%m-%d')

    oldcommit = json.loads(requests.get('https://api.github.com/repos/' + orgname + '/' + repo + "/commits?until=" + week_before + "T05:00:00Z&access_token=" + xxx).text)
    newcommit = json.loads(requests.get('https://api.github.com/repos/' + orgname + '/' + repo + "/commits?since=" + week_before + "T15:50:00Z&until="+ now + 'T05:00:00Z&access_token=' + xxx).text)

    if newcommit == []:
        return None
    elif oldcommit == []:
        return (None, newcommit[0]["sha"])
    else:
        return (oldcommit[0]["sha"], newcommit[0]["sha"])

#Receive the list of SHAs, find all files in their repo past week and this week and get the files that were created this week
def getNewFiles():
    global gitHubgrades
    oldfiles = []
    newfiles = []
    for repo in [r for r in getRepo("name") if not r in ["A", "list", "of", "repos", "not", "to", "delete"] and r[:len("project")] != "project"]:
        shas = getSHA(repo)

        if shas == None:
            gitHubgrades[repo] = '0'
            continue
        elif not shas[0] == None:
            old = json.loads(requests.get('https://api.github.com/repos/' + orgname + '/' + repo + '/git/trees/' + shas[0] + '?access_token=' + xxx + "&recursive=1").text)
            for fileInfo in old["tree"]:
                filePath = repo + "/" + fileInfo["path"]
                oldfiles.append(filePath)
        new = json.loads(requests.get('https://api.github.com/repos/' + orgname + '/' + repo + '/git/trees/' + shas[1] + '?access_token=' + xxx + "&recursive=1").text)
        print(new)
        for fileInfo in new["tree"]:
            if fileInfo["type"] == "blob":
                filePath = repo + "/" + fileInfo["path"]
                if filePath not in oldfiles:
                    print(int(fileInfo["size"]), filePath)
                    if int(fileInfo["size"]) > 5 and not filePath == ".gitignore":
                        gitHubgrades[repo] = '1'
                        newfiles.append(filePath)
                    else:
                        if filePath == ".gitignore":
                            gitHubgrades[repo] = '0 ' + 'EmptyFile: ' + filePath
    return newfiles

def plager(fileone, filetwo):
    return 0

def getGrades():
    global gitHubgrades
    ProjectSnapShots.backup()
    files = getNewFiles()

    for out in range(len(files)):
        for inn in range(len(files)):
            if plager(files[out], files[inn]):
                print("Cheaters; Files:", files[out], files[inn])
                gitHubgrades[files[out].split('/')[0]] = '0 Plagerism Detected'
                gitHubgrades[files[inn].split('/')[0]] = '0 Plagerism Detected'

    f = open(st + '/reasoning.t', 'w')
    for i in gitHubgrades.items():
        f.write(str(i))
        f.write('\n')
    f.close()

    for i in gitHubgrades.items():
        gitHubgrades[i[0]] = int(i[1][0])