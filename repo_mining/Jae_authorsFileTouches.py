import requests
import json
import csv
import os

def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lsttoken)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

def collect_authors_and_dates(dictfiles, lsttokens, repo):
    ipage = 1  # Page counter
    ct = 0  # Token counter
    author_date_dict = {}

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if not jsonCommits:
                break

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if filename in dictfiles:
                        if filename not in author_date_dict:
                            author_date_dict[filename] = []
                        author_date_dict[filename].append((author, date))
            ipage += 1
    except Exception as e:
        print("Error receiving data", e)
        exit(0)

    return author_date_dict


# Repository and tokens (replace with your own)
repo = 'scottyab/rootbeer'
lstTokens = [""]

# Example source files dictionary from the modified CollectFiles.py script
source_files = {'file1.java': 3, 'file2.cpp': 2}  # Replace with actual data

# Collect authors and dates
authors_dates = collect_authors_and_dates(source_files, lstTokens, repo)

# Save to CSV
output_file = f'data/{repo.split("/")[1]}_authors_dates.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Author", "Date"])
    for filename, touches in authors_dates.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f'Data saved to {output_file}')
