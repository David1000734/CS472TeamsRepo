import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttokens, ct):
    jsonData = None
    try:
        ct = ct % len(lsttokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct

# Filter source files based on extensions
def is_source_file(filename):
    source_extensions = ['.java', '.kt', '.cpp', '.c', '.cmake']  # Extensions for Java, Kotlin, C++, C, CMake
    return any(filename.endswith(ext) for ext in source_extensions)

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    
                    # Only process source files
                    if is_source_file(filename):
                        dictfiles[filename] = dictfiles.get(filename, 0) + 1
                        print(filename)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'
repo = 'scottyab/rootbeer'

# put your tokens here
lstTokens = ["fake_token1",
                "fake_token2",
                "fake_token3"]

# Function call to count files
dictfiles = {}
countfiles(dictfiles, lstTokens, repo)
print(f'Total number of source files: {len(dictfiles)}')

# Output file setup
file = repo.split('/')[1]
fileOutput = f'data/file_source{file}.csv'

with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Touches"])

    # Find the file with the maximum touches while writing rows to CSV
    bigfilename, bigcount = max(dictfiles.items(), key=lambda x: x[1], default=(None, None))
    
    for filename, count in dictfiles.items():
        writer.writerow([filename, count])

print(f'The file {bigfilename} has been touched {bigcount} times.')
