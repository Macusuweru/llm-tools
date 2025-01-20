import os
import anthropic

file = "main.txt"
main_directory = "docs"
try:
    with open(os.path.dirname(__file__) + "/system-prompts/" + file, "r") as file:
        system = file.read()
except FileNotFoundError:
    print(f"The file '{file}' was not found in the script directory.")

try:
    with open(os.path.dirname(__file__) + f"/{main_directory}/main.txt", "r") as file:
        system += f"\n +++ \n{file.read()}\n+++"
except FileNotFoundError:
    print(f"The file '{file}' was not found in the script directory.")

opus3p0 = "claude-3-opus-20240229"
sonnet3p5 = "claude-3-5-sonnet-20241022"
haiku3p5 = "claude-3-5-haiku-20241022"
model = sonnet3p5

system += "\nYou are " + model

tools = [
    {
        "name": "calendarAdd",
        "description": "A tool to add events to a calendar",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    ""
                    "description": "The category the event will be stored in the calendar under."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the event. A 2-5 word description if none is given "
                },
                "start": {
                    "type": "string",
                    "description": "The start time of the event."
                },
                "length": {
                    "type": "string",
                    "description": "The length of the event."
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event, if any is given or implied."
                },
            },
            "required": ["category"]
        }
    },{
        "name": "calendarRead",
        "description": "A tool to read events in the calendar within a range",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The category the event will be stored in the calendar under."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the event. A 2-5 word description if none is given "
                },
                "start": {
                    "type": "string",
                    "description": "The start time of the event."
                },
                "length": {
                    "type": "string",
                    "description": "The length of the event."
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event, if any is given or implied."
                },
            },
            "required": ["expression"]
        }
    },{
        "name": "write",
        "description": "An interface to write text files or code.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text you want to write into the file."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the file to write to. Creates a new file if necessary. Use an arbitrary filename if necessary."
                },
                "overwrite": {
                    "type": "boolean",
                    "description": "True to overwrite the entire file. False to add the text to the end of the file. Default to False."
                }
            },
            "required": ["text", "name", "overwrite"]
        }
    }, {
        "name": "read",
        "description": "An interface to read text files.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the file you wish to read. If the file does not exist, this will return n/a."
                }
            },
            "required": ["name"]
        }
    }, {
        "name": "ls",
        "description": "Return all contents of the given directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory. Use empty string for the main directory."
                }
            },
            "required": ["directory"]
        }
    }, {
        "name": "time",
        "description": "Returns the current time.",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }, {
        "name": "makeDir",
        "description": "Create a new directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name."
                },
                "directory": {
                    "type": "string",
                    "description": "The location of the new directory. Empty string is legal."
                }
            },
            "required": ["name", "directory"]
        }
    }
]

# Define the directory path for text files
TEXT_DIR = os.path.join(os.path.dirname(__file__), f"{main_directory}")

# Ensure the "text" directory exists
os.makedirs(TEXT_DIR, exist_ok=True)

def write(text, name, overwrite=False):
    """
    Writes to a text file in the "text" directory.
    
    Parameters:
        text (str): The text to write into the file.
        name (str): The name of the file.
        overwrite (bool): If True, overwrites the file; otherwise, appends to it.
    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    if not name or not text:
        return "Both 'text' and 'name' are required."
    
    file_path = os.path.join(TEXT_DIR, name)
    mode = "w" if overwrite else "a"  # Write or append mode
    
    try:
        with open(file_path, mode) as file:
            file.write(text)
        return f"Text written to '{name}'."
    except Exception as e:
        return f"Failed to write to file. Error: {e}"


def read(name):
    """
    Reads a text file in the "text" directory.
    
    Parameters:
        name (str): The name of the file to read.
    Returns:
        dict: A dictionary with the status, message, and file content or list of files.
    """

    file_path = os.path.join(TEXT_DIR, name)
    if not os.path.exists(file_path):
        return f"File '{name}' does not exist."
    
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Failed to read file. Error: {e}"

def ls(directory, separator = "\n"):
    """
    Returns a string listing out all files and directories in the given directory
    
    Parameters:
        directory (string): the directory to read all files from
        separator (string): default \n (newline). String which separates resulting list of filenames.
    Returns:
        string: a string containing the names of all files, seperated by the seperation character"""
    try:
        files = os.listdir(directory)
        return separator.join(files,) if files else f"No files found in the '{directory}' directory."
    except Exception as e:
        return f"Failed to list files. Error: {e}"
    
def get_current_time():
    from datetime import datetime
    return datetime.now().strftime("%B %d, %Y %I:%M %p")



client = anthropic.Anthropic()

print("Your name:")
name = input()

print("Tool use?")
tool_message = [{"role": "user", "content":input()}]
tool_use = (client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=10,
        temperature=0,
        system="Return exactly \"True\" or \"False\" depending on whether the message is positive or negative. Default to \"False\" if uncertain.",
        messages=tool_message
    ).content[0].text) == "True"

chat=[]
tool_stack = []
print(name + ": ")
first_message = name + ": " + input()
chat.append({"role": "user", "content": first_message})
while True:
    if (tool_use):
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0,
            system=system,
            messages=chat,
            tools=tools
        )
    else:
        message = client.messages.create(
            model=model,
            max_tokens=1000,
            temperature=0,
            system=system,
            messages=chat
        )

    content = ""

    for block in message.content:
        if block.type == "text":
            content += block.text
        elif block.type == "tool_use":
            tool_stack.append(block)

    chat.append({"role": "assistant", "content": f"{content}"})
    print(f"{model}: {content}")

    response = []
    
    for block in tool_stack:
        if (block.name == "write"):
            response.append(f"SYSTEM >>> WRITE {block.input["text"]} TO {block.input["name"]} RETURNS {write(block.input["text"], block.input["name"], block.input["overwrite"])}\n")
        elif (block.name == "read"):
            response.append(f"SYSTEM >>> READ {block.input["name"]} RETURNS {read(block.input["name"])}\n")
        elif (block.name == "ls"):
            response.append(f"SYSTEM >>> LS {block.input["directory"]} RETURNS {ls(os.path.join(TEXT_DIR, block.input["directory"]))}\n")
        elif (block.name == "time"):
            response.append(f"SYSTEM >>> TIME RETURNS {get_current_time()}\n")
        elif (block.name == "makeDir"):
            response.append(f"SYSTEM >>> MAKEDIR {block.input["directory"]}/{block.input["name"]} RETURNS \"Directory created\"\n")
            os.makedirs(os.path.join(TEXT_DIR, block.input["name"]), exist_ok=True)
        else:
            response.append("SYSTEM >>> ERROR: TOOL NOT AVAILABLE")
    tool_stack = []

    if (message.stop_reason != "tool_use"):
        user = input()
        if user == "end": break
        response.append(f"{name}: \"{user}\"\n")
    
    print("\n".join(response))
    chat.append({"role": "user", "content": "\n".join(response)})


