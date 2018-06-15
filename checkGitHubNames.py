import requests

print("This assumes a csv of uniqueIdentifier,GitHubUsername")

def uid_github():
  lines = open('githubroster.txt', 'r').readlines()

  filtered = []

  for line in lines:
    filtered.append((line.split('\t')[0], line.split('\t')[1][:-1]))

  return filtered

for uid,username in uid_github():
  if requests.get("http://www.github.com/" + username).status_code == 404:
    print(username, uid)
  else:
    print(".", end="")
