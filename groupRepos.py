#!/usr/bin/python3

from subprocess import call

xxx = input("Github API Key: ")
GitHubUser = input("Github API Key: ")
orgname = input("Organization Name: ")

# Given a list of people, make their repo
# team = [("abc123", "Kyle Martin"), ("cba3210", "Catty Chool"), ("dfv623", "Mickfly"), ("sdf038", "Jonny Money")]
def makeRepo(team, projectTitle=''):
    teamName = ("".join(projectTitle.split(" "))).lower()
    names = ""
    for ID,name in team:
        teamName += "-" + ID
        names += name + ", "
    names = names[:-2]
    names = ",".join(names.split(',')[:-1] + [" and" + names.split(',')[-1]])

    command = '''curl -H 'Authorization: token ''' + xxx + '''' -d '{ "name": "''' + teamName + '''", "description": "The ''' + projectTitle + ''' group repo for ''' + names +  '''.", "private": true, "has_issues": true, "has_projects": false, "has_wiki": false }' "https://api.github.com/orgs/''' + orgname + '''/repos"'''

    # print(command)
    call(command, shell=True)

# Given a list of people, share the repo with each of them
def shareRepo(team, projectTitle=''):
    teamName = ("".join(projectTitle.split(" "))).lower()
    names = ""
    for ID,name in team:
        teamName += "-" + ID
        names += name + ", "
    names = names[:-2]
    names = ",".join(names.split(',')[:-1] + [" and" + names.split(',')[-1]])

    for ID,name in team:
        gitHubUsername = lookupTable[ID]

        command = '''curl -i -u "''' + GitHubUser + ':' + xxx + '''" -X PUT -d '' 'https://api.github.com/repos/''' + orgname + '/' + teamName + '''/collaborators/''' + gitHubUsername + "'"
        # print(command)
        call(command, shell=True)
