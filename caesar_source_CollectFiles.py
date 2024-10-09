import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttokens, ct):
    """
    Authenticate requests to the GitHub API using a list of tokens.

    Args:
        url (str): The GitHub API URL to send the request to.
        lsttokens (list): List of GitHub authentication tokens.
        ct (int): The current index of the token to use for authentication.

    Returns:
        tuple: A tuple containing the JSON response from the API and the updated token index.

    Notes:
        If an error occurs during the request, it will be printed, and the function will return None.
    """
    jsonData = None
    try:
        ct = ct % len(lsttokens)  # Cycle through tokens
        headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print(e)
    return jsonData, ct

# Filter source files based on extensions
def is_source_file(filename):
    """
    Check if a file is a source file based on its extension.

    Args:
        filename (str): The name of the file to check.

    Returns:
        bool: True if the file is a source file, False otherwise.

    Notes:
        Source files are identified by their extensions: '.java', '.kt', '.cpp', '.c', and '.cmake'.
    """
    source_extensions = ['.java', '.kt', '.cpp', '.c', '.cmake']
    return any(filename.endswith(ext) for ext in source_extensions)

# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def countfiles(dictfiles, lsttokens, repo):
    """
    Count the number of times source files in a GitHub repository have been modified (touched) across commits.

    Args:
        dictfiles (dict): A dictionary to store file names and their modification counts.
        lsttokens (list): List of GitHub authentication tokens.
        repo (str): The GitHub repository in the format 'owner/repo' to analyze.

    Returns:
        None

    Notes:
        This function paginates through all commits in the repository, checking which source files were modified in each commit.
        The results are stored in the 'dictfiles' dictionary, where the key is the file name and the value is the number of times it was touched.
    """
    ipage = 1  # Page counter for commits API pagination
    ct = 0  # Token counter to cycle through tokens

    try:
        # Loop through commit pages until no more commits are returned
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # Break loop if no more commits are found
            if len(jsonCommits) == 0:
                break

            # Iterate through commits to find modified files
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']

                    # Only count source files
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
