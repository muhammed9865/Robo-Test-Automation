import requests
import json
import sys
import os


# get the input file
input_file = sys.argv[1]
# get the slack webhook url
slack_webhook_url = sys.argv[2]
if len(sys.argv) > 3:
    app_version = sys.argv[3]
else:
    app_version = ""

# the input file is a json file in the format of [ { "axis_value": "Pixel3-30-en-portrait", "outcome": "Passed", "test_details": "--" } ]
# read the input file
with open(input_file) as f:
    data = json.load(f)
    # format the json to be like
    # <b>Test Details</b>
    # Device: Pixel3-30-en-portrait - <green>Passed</green>
    # Device: Pixel3-30-en-portrait - <red>Failed</red>
    # Device: Pixel3-30-en-portrait - <yellow>Skipped</yellow>
    
    message = ""
    if app_version != "":
        message += "> *Version*\n"
        message += "> " + app_version + "\n"

    message += "> *Test Details*\n"
    for item in data:
        name = item["axis_value"]
        outcome = item["outcome"]
        if outcome == "Passed":
            mark = ":white_check_mark:"
        elif outcome == "Failed":
            mark = ":x:"
        else:
            mark = ":warning:"
        message += "> Device: " + name + " - " +  outcome + " " + mark + "\n"

    payload = {
        "text": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(slack_webhook_url, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        print(f"Error sending message to Slack: {response.text}")
    else:
        print("Message sent successfully!")
