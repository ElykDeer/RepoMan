#!/usr/bin/env python3

import string
from subprocess import call
import json
import requests
from datetime import datetime
import threading

##################$##
# Make sure to add  #
#  to this list     #
#  anything you do  #
#  not want deleted #
#  from the org.    #
#####################
filterList = ['SuperImportantRepo', 'PlsDontDeleteMe']

orgname = "MyVerySpecialOrganization"

st = datetime.now().strftime('%Y-%m-%d')

xxx = input("Access token (https://github.com/settings/tokens/new): ")
GitHubUser = input("GitHub Username: ")

menu = '''Menu:
    1. Delete all repos
    2. Delete all project repos
    3. Delete all personal repos
Choice:
'''
ans = input(menu)

# Returns a list a given element from all git repos (ie, all of their ssh_url's)
def getRepo(element):
    data = []
    for page in range(1, 100): # Technically limited to 10,000 repos, but come on.
        # Get next page of repos
        responce = json.loads(requests.get('https://api.github.com/orgs/' + orgname + '/repos?per_page=500&access_token=' + xxx + '&page=' + str(page)).text)
        for d in responce:
            data.append(d[element])

        # Stop when there are no more repos
        if responce == []:
            break

    return data

# Backup all repos in gits/ and put a listing of all of them in ./repos.txt
def backupGroup(group):
    for repo in group:
        command = "cd /tmp/" + st + "; git clone https://" + GitHubUser + ":" + xxx + "@github.com/" + repo
        call(command, shell=True)

def backup():
    call("mkdir /tmp/" + st, shell=True)
    repos = getRepo("full_name")
    workers = 8

    threads = [threading.Thread(target=backupGroup, args=[repos[i::workers]]) for i in range(workers)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    command = "ls /tmp/" + st + "/ > repos.txt"
    call(command, shell=True)

def getList(filt):
    people = open("repos.txt", 'r').readlines()
    for i in range(len(people)):
        people[i] = "".join([c for c in people[i] if c in string.ascii_letters + string.digits + '-'])
    people = [repo for repo in people if repo not in filt]
    return people

def confirmDelete():
    ans = input("Done backing up, continue to deleting? [y/N]")
    if ans != "y" and ans != "Y":
        quit()

if ans == '1':
    ans = input("Finally, verify that the only things you want filtered are: " + str(filterList) + "\nContinue? [y/N] ")
    if ans != "y" and ans != "Y":
        quit()

    print("Backing up")
    backup()

    confirmDelete()

    for repo in getList(filterList):
        command = "curl -XDELETE -H 'Authorization: token " + xxx + "' https://api.github.com/repos/" + orgname + "/" + repo
        print(command)
        call(command, shell=True)

elif ans == '2':
    print("Backing up")
    backup()

    confirmDelete()

    for repo in getList(filterList):
        if repo[:len("project")] == "project":
            print(repo)
            command = "curl -XDELETE -H 'Authorization: token " + xxx + "' https://api.github.com/repos/" + orgname + "/" + repo
            call(command, shell=True)

elif ans == '3':
    print("Backing up")
    backup()

    confirmDelete()

    for repo in getList(filterList):
        if not repo[:len("project")] == "project":
            command = "curl -XDELETE -H 'Authorization: token " + xxx + "' https://api.github.com/repos/" + orgname + "/" + repo
            print(command)
            call(command, shell=True)

else:
    print("Ahhh")
    quit()
