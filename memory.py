tags = {
    "children": {
        "Tools": {
            "start": "<tool>",
            "end": "</tool>",
            "children": {
                "Tool1": {
                    "start": "<tool1>",
                    "end": "</tool1>",
                    "children": {
                        "arg1": {"start": "<arg1=\"", "end": "\">"},
                        "arg2": {"start": "<arg2=\"", "end": "\">"},
                    }
                },
                "Tool2": {
                    "start": "<tool2>",
                    "end": "</tool2>",
                    "children": {
                        "arg1": {"start": "<arg1=\"", "end": "\">"},
                        "arg2": {"start": "<arg2=\"", "end": "\">"},
                    }
                }
            }
        },
        "Examples": {
                    "start": "<examples>",
                    "end": "</examples>",
                    "children": {
                        "<basic>": {"start": "<basic>", "end": "</basic>"},
                        "<advanced>": {"start": "<advanced>", "end": "</advanced>"},
                        "<errors>": {"start": "<errors>", "end": "</errors>"}
                    }
                }
            }
        }


def parse_recursive(input_text, current_tag):
    results = {}
    for name, specs in current_tag["children"].items():
        pos = 0
        while True:
            start_text = specs["start"]
            end_text = specs["end"]

            # Find start of current tag
            start = input_text.find(start_text, pos)
            if start == -1:
                break
                
            # Find end marker
            end = input_text.find(end_text, start + len(start_text))
            if end == -1:
                break
                
            content = input_text[start + len(start_text):end]
            
            # Recursively parse nested tags if they exist
            if "children" in specs:
                results[name] = parse_recursive(content, specs)
            else:
                results[name] = content
            
            pos = end + len(end_text)
            
    return results

def tool1(arg1, arg2):
    print("tool1")
    print(arg1)
    print(arg2)
    return

def tool2(arg1, arg2):
    print("tool2")
    print(arg1)
    print(arg2)
    return

def run_tools(parsed):
    for name1, content1 in parsed.items():
        if name1 == "Tools":
            for name2, content2 in content1.items():
                if name2 == "Tool1":
                    arg1 = "fail1"
                    arg2 = "fail2"
                    for name3, content3 in content2.items():
                        if name3 == "arg1":
                            arg1 = content3
                        if name3 == "arg2":
                            arg2 = content3
                    tool1(arg1, arg2)
                if name2 == "Tool2":
                    arg1 = "fail3"
                    arg2 = "fail4"
                    for name3, content3 in content2.items():
                        if name3 == "arg1":
                            arg1 = content3
                        if name3 == "arg2":
                            arg2 == content3
                    tool2(arg1, arg2)




test = """
<tool> 
    <tool1>
        <arg1="plus1">
        <arg2="plus2">
    </tool1>
</tool>
<examples>
    <basic> Whatever </basic>
</examples>
"""

parsed = parse_recursive(test, tags)
print(parsed)
run_tools(parsed)