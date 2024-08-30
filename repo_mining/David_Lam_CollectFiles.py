import json
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
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
    global authorCount

    try:
        ignore_Files = [
            ".pdf",
            ".xml",
            ".htlm",
            ".css",
            ".log",
            ".txt",
            ".json",
            ".js",
        ]

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
                author = shaDetails["commit"]["author"]

                # We must avoid overwritting data if it currently exist in our dictionary.
                # Only initilize the author's name if one does not currently exist.
                if author["name"] not in authorCount:
                    # Initilize each author's name to a empty dictionary
                    authorCount[author["name"]] = dict()

                for idx, filenameObj in enumerate(filesjson):
                    filename = filenameObj['filename']

                    # Due to the nature of this dictionary, we will have to access it a little wierdly
                    # First, we much attempt to find a file under the authors name      (author["name"][filename])
                    #   if one does not exist, a new dictionary entry will be created
                    # Then, get whatever value is in there      authorCount[author["name"]].get(filename, 0)
                    #   and increment it. 
                    authorCount[author["name"]][filename] = authorCount[author["name"]].get(filename, 0) + 1

                    # Ignore all non "source" files
                    if not any(filename.endswith(x) for x in ignore_Files):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        # print file name, author, as well as time for each file modified
                        print("File: %s\nAuthor: %s, committed: %s\n" % \
                             (filename, author["name"], pd.to_datetime(author["date"], utc = True)))
                    
                    if idx > 10:
                        print("BREAKING")
                        return       # DEBUG

            ipage += 1
    except Exception as e:
        print("Error receiving data")
        print("Exception: %s" % e)
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
lstTokens = ["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",
                "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",
                "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"]

dictfiles = dict()

# We will have to keep track of the author, which files they modified,
# as well as how many times they modified that file. We will do this by using
# a dictionary of dictionarys.
# The first dictionary will be Dictionary<AuthorName, Dictionary<filename, count>>
# or    "authorName": {"filename": "count for file"}
authorCount = dict()

countfiles(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
# change this to the path of your file
fileOutput = 'data/file_' + file + '.csv'
rows = ["Filename", "Touches"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

bigcount = None
bigfilename = None
for filename, count in dictfiles.items():
    rows = [filename, count]
    writer.writerow(rows)
    if bigcount is None or count > bigcount:
        bigcount = count
        bigfilename = filename

fileCSV.close()
print('The file ' + bigfilename + ' has been touched ' + str(bigcount) + ' times.')

# Start to build the graphs
fig = plt.figure()
ax1 = fig.add_subplot(111)

# Iterate through our array of authors
for key, fileDict in authorCount.items():
    data = list(fileDict.items())
    fileValue = []

    # Will not be displaying the file name, instead they will be represented as numbers.
    for idx, dictValue in enumerate(data):
        # First file is 1, next is 2, etc.
        fileValue.append(idx + 1)

    # Build the X axis with the numeric value of the file names
    x = np.array(list(fileValue))
    # BUild the Y axis with the count of each file
    y = np.array(list(fileDict.values()))

    # NOTE: Each iteration is for each author. Place the found count, etc
    # for each other. 
    ax1.scatter(x, y, label = key, alpha = 0.6)

plt.xlabel("file")
plt.ylabel("weeks")
plt.legend()
plt.show()
