import requests
import json
import sys


def fix_input_text(data: list) -> str:
    # Convert the input JSON string to a Python list
    input_list = json.loads(data)

    # Create a new list to store the fixed format dictionaries
    output_list = []

    # Iterate over each dictionary in the input list
    for item in input_list:
        # Extract the values from the dictionary
        axis_value = item['axis_value']
        outcome = item['outcome']
        test_details = item['test_details']

        # Create a new dictionary in the correct format
        new_item = {
            'axis_value': axis_value,
            'outcome': outcome,
            'test_details': test_details
        }

        # Append the new dictionary to the output list
        output_list.append(new_item)

    # Convert the output list to JSON string in the correct format
    output_json = json.dumps(output_list, indent=4)

    return output_json

def prepare_message(data, app_name, app_version) -> str:
    message = ""
    
    if app_name != "":
        app_details = app_name
        if app_version != "":
            app_details += " - " + app_version
    
    if app_details != "":
        message += "> *Version*\n"
        message += "> " + app_details + "\n"

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


#### Script starts here ####

# get the input file
input_file = sys.argv[1]

# get the slack webhook url
slack_webhook_url = sys.argv[2]

# get the app name
if len(sys.argv) > 3:
    app_name = sys.argv[3]
else:
    app_name = ""

# get the app version
if len(sys.argv) > 4:
    app_version = sys.argv[4]
else:
    app_version = ""

with open(input_file) as f:
    try:
        print("Reading input file...")
        input = f.read()
        fixed_input = fix_input_text(input)

        last_input = fixed_input

        print(f"Input: {input}")
        print(f"Fixed input: {last_input}")
        
        data = json.loads(last_input)
        
        message = prepare_message(data, app_name, app_version)

        print("Sending message to Slack...")
        send_message(message)

        
    except Exception as e:
        print("Error reading input file or sending message to Slack: " + str(e))
        
