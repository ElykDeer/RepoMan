#!/usr/bin/env python3

import string
from subprocess import call
import json
import requests
import smtplib
from datetime import datetime, timedelta
import threading

GitHubUser = ""
xxx = ''
orgname = ""

st = datetime.now().strftime('%Y-%m-%d')

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

def notify(messageSender, password, TO):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(messageSender, password)

    BODY = 'The GitHub backup is ready!'

    server.sendmail(messageSender, TO, BODY)

def backup():
    call("mkdir /tmp/" + st, shell=True)
    repos = getRepo("full_name")
    workers = 8

    threads = [threading.Thread(target=backupGroup, args=[repos[i::workers]]) for i in range(workers)]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    command = "zip -r " + st + ".zip /tmp/" + st
    call(command, shell=True)
