import json
from datetime import datetime
import argparse
import os

#get directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

#Set arguments
parser = argparse.ArgumentParser()
parser.add_argument("--input", help = "The Oggabooga Chat to convert")
parser.add_argument("--output", help = "The Chat output for Sillytavern")
parser.add_argument("--yourname", help = "Your name")
parser.add_argument("--charname", help = "Your Character's name")
args = parser.parse_args()

print("#Now Converting")
print('#The Oggabooga file to be converted:', args.input)
print('#The output file name for sillytavern:', args.output)
print('#Your name:', args.yourname)
print("#The character's name:", args.charname)

# @markdown **Character Names**
user_name = args.yourname  # @param {type: "string"}
ai_name = args.charname  # @param {type: "string"}

# @markdown **Input File:** Fill thise field only if you have already uploaded the file in the colab storage, else leave it blank - you will be asked to choose file during runtime if the file is not found in your specified path.
upload_input_file = False
input_file_path = args.input  # @param {type: "string"}

# @markdown **Output File Name**
output_file_name = args.output  # @param {type: "string"}


intermediate_output_file_name = "intermediate_output"

# the first line with necessary metadata
inserted_line = {
    "user_name": user_name,
    "character_name": ai_name,
    "create_date": datetime.now().strftime("%Y-%m-%d@%Hh%Mm%Ss"),
    "chat_metadata": {
        "note_prompt": "",
        "note_interval": 1,
        "note_position": 1,
        "note_depth": 4
    }
}

# Part 1: Extracts the chat from the visible section of your ooba chat history and stores it in another JSON file
def extract_visible_chat(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        data = json.load(input_file)
        visible_data = data.get('visible', [])
        json.dump(visible_data, output_file)

# Part 2: Reads the generated JSON file and converts it into a format that matches the structure of Sillytavern chat history
def generate_message(name, is_user, message, extra=None):
    if not message.strip():
        return None  # Skip entries with empty messages

    current_time = datetime.now().strftime("%B %d, %Y %I:%M%p")
    output = {
        "name": name,
        "is_user": is_user,
        "send_date": current_time,
        "mes": message,
        "extra": extra if extra else {}
    }
    if is_user:
        output["force_avatar"] = "User Avatars/user-default.png"
    return json.dumps(output, indent=4)

def process_input_file(input_messages, output_file_path, user_name, ai_name):
    with open(output_file_path, 'w') as output_file:
        for messages in input_messages:
            user_message = messages[0]
            ai_message = messages[1]

            user_output = generate_message(user_name, True, user_message, {})
            ai_output = generate_message(ai_name, False, ai_message, {
                "gen_started": "2023-11-09T06:12:56.823Z",
                "gen_finished": "2023-11-09T06:13:23.457Z",
                "swipe_id": 0,
                "swipes": [ai_message],
                "swipe_info": [
                    {
                        "send_date": "November 9, 2023 11:43am",
                        "gen_started": "2023-11-09T06:12:56.823Z",
                        "gen_finished": "2023-11-09T06:13:23.457Z",
                        "extra": {
                            "api": "textgenerationwebui",
                            "model": "TheBloke_echidna-tiefigther-25-GPTQ"
                        }
                    }
                ]
            })

            if user_output:
                output_file.write(user_output + '\n\n')
            if ai_output:
                output_file.write(ai_output + '\n\n')

# Part 3: Generates a final output file with .jsonl extension which can be used in sillytavern
def convert_json_to_jsonl(input_file_path, output_file_path):
    with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
        data = ""
        for line in infile:
            data += line.strip()
            try:
                json_data = json.loads(data)
                formatted_json = json.dumps(json_data, separators=(',', ':')) + '\n'
                outfile.write(formatted_json)
                data = ""
            except json.JSONDecodeError:
                pass

# Modification Part: Modifies the first line of the generated .jsonl file
def modify_first_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines:
        first_line = json.loads(lines[0])
        first_line['is_system'] = False
        first_line['send_date'] = "November 9, 2023 11:40am"
        first_line['extra'] = {}
        first_line = {k: first_line[k] for k in ['name', 'is_user', 'is_system', 'send_date', 'mes', 'extra']}

        lines[0] = json.dumps(first_line) + '\n'

        with open(file_path, 'w') as file:
            file.writelines(lines)

# Process the input file
extract_visible_chat(input_file_path, dir_path + '/content/pre-intermediate-output.json')
input_messages = json.load(open(dir_path + '/content/pre-intermediate-output.json', 'r'))
intermediate_output_file_path = dir_path + f"/content/{intermediate_output_file_name}.jsonl"
process_input_file(input_messages, dir_path + '/content/pre-intermediate-output.json', user_name, ai_name)
convert_json_to_jsonl(dir_path + '/content/pre-intermediate-output.json', intermediate_output_file_path)
modify_first_line(intermediate_output_file_path)

# Insert line at the beginning of the final output file
input_file_path = intermediate_output_file_path
output_file_path = dir_path + f"/{output_file_name}.jsonl"

with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
    # Insert the line at the beginning
    outfile.write(json.dumps(inserted_line) + '\n')

    # Shift all lines down by one line
    for line in infile:
        outfile.write(line)
