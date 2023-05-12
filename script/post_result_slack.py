import requests
import json
import sys
import os


# get the input file
input_file = sys.argv[1]

# get the slack webhook url
slack_webhook_url = sys.argv[2]

# get the app version
if len(sys.argv) > 3:
    app_version = sys.argv[3]
else:
    app_version = ""


def fix_input_text(data: list) -> str:
    new_data = ""
    for line in data:
        if line.startswith("["):
            new_data += "[\n" + line[1:] + "\n"
    
    return new_data

def prepare_message(data) -> str:
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
    
    return message


def send_message(message: str):
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


with open(input_file) as f:
    try:
        print("Reading input file...")
        input = f.readlines()
        fixed_input = fix_input_text(input)

        print(f"Input: {input}")
        print(f"Fixed input: {fixed_input}")
        
        data = json.loads(fixed_input)
        
        message = prepare_message(data)

        print("Sending message to Slack...")
        send_message(message)

        
    except Exception as e:
        print("Error reading input file or sending message to Slack: " + str(e))
        
