import json
import requests
import csv
import numpy as np

import os

if not os.path.exists("data"):
 os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    global authorTouches 
    authorTouches = [[]]
    global tempArr
    tempArr = []
    # source file extensions
    goodFiles = [".cpp", ".java", ".h", ".kt", ".c"]

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                # gets autho name, date of commit, and email
                author = shaDetails["commit"]["author"]
                
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    
                    # if the file is a source file, add author, date and filename to array
                    if any(filename.endswith(x) for x in goodFiles):
                        tempArr=[author["name"], author["date"], filename]
                        print(tempArr)
                        authorTouches.append([author["name"], author["date"], filename]);
                        tempArr.clear()
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)
# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'


# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print("\n\n\n")
print(authorTouches[1])
print(authorTouches[1][0])
for i in range(1, len(authorTouches)):
    print(i)
    print("name:", authorTouches[i][0])
    print("date:", authorTouches[i][1])
    print("file:", authorTouches[i][2])
print('Total number of files: ' + str(len(dictfiles)))

fileOutput = 'data/author_touches.csv'
rows = ["Name", "Date", "File"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for i in range(1, len(authorTouches)):
    rows = [authorTouches[i][0], authorTouches[i][1], authorTouches[i][2]]
    writer.writerow(rows)
fileCSV.close()
print("DONE!")

# file = repo.split('/')[1]
# # change this to the path of your file
# fileOutput = 'data/file_' + file + '.csv'
# rows = ["Filename", "Touches"]
# fileCSV = open(fileOutput, 'w')
# writer = csv.writer(fileCSV)
# writer.writerow(rows)

# bigcount = None
# bigfilename = None
# for filename, count in dictfiles.items():
#     rows = [filename, count]
#     writer.writerow(rows)
#     if bigcount is None or count > bigcount:
#         bigcount = count
#         bigfilename = filename
# fileCSV.close()
# print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')
