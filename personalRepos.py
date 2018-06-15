#!/usr/bin/python3
from subprocess import call
import csv

debug = True

xxx = input("Github API Key: ")
orgname = input("Organization Name: ")

# Read in net id's and names
uids = []
if not debug:
    ans = input("This bit assumes that roster.csv exists as 'NetID','Lastname, Firstname'\nContinue? [y/N] ")
    if ans != 'y' and ans != 'Y':
        print("okaybye")
        quit()

# Assumes that there's a 'roster.csv' with two collumns as (uid, "Lastnames, Firstnames")
uids=[]
with open('roster.csv') as f:
    uids=[tuple(line) for line in csv.reader(f)]
for i in range(len(uids)): # Fix names
    uids[i] = (uids[i][0], uids[i][1].split(', ')[1] + ' ' + uids[i][1].split(',')[0])

call("mkdir ../temp/", shell=True)
for ID,name in uids:
    command = '''curl -H 'Authorization: token ''' + xxx + '''' -d '{ "name": "''' + ID + '''", "description": "The repo for ''' + name + ''' to submit reports", "private": true, "has_issues": true, "has_projects": false, "has_wiki": false }' "https://api.github.com/orgs/''' + orgname + '/repos"'
    call(command, shell=True)
    command = "cd ../temp/; git clone git@github.com:" + orgname + "/" + ID
    call(command, shell=True)
    command = "cp personalReposreadme.md ../temp/" + ID + "/readme.md"
    call(command, shell=True)
    command = "cd ../temp/" + ID + "; git add readme.md; git commit -m 'Initial Commit'; git push"
    call(command, shell=True)

call("rm -r ../temp/", shell=True)
