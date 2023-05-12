# write a script to get the input file and clean the result file and post the result to slack

import os
import sys
import json
import requests

# get the input file
input_file = sys.argv[1]

# the input file is the result file, so we need to clean it
# read the file
with open(input_file, 'r') as f:
    lines = f.readlines()
    firstLetterToCheck = '┌'
    latestLetterToCheck = '┘'
    # get all the text between the firstLetterToCheck and latestLetterToCheck
    # and write it to a new file
    new_lines = []
    for line in lines:
        if firstLetterToCheck in line:
            start = lines.index(line)
        if latestLetterToCheck in line:
            end = lines.index(line)
        
    new_lines = lines[start:end+1]
    # write the new lines to a new file
    with open('cleaned_result.txt', 'w') as f:
        for line in new_lines:
            f.write(line)
    
# post the result to slack
# get the slack webhook url from the args
slack_webhook_url = sys.argv[2]
# read the cleaned result file
with open('cleaned_result.txt', 'r') as f:
    lines = f.readlines()
    # get the text from the file
    text = ''
    for line in lines:
        text += line
    # post the text to slack
    payload = {
        'text': text
    }
    requests.post(slack_webhook_url, json.dumps(payload))