import os


tags = {
    "children": {
        "Memory": {
            "start": "<memory>",
            "end": "</memory>",
            "children": {
                "Read": {
                    "start": "<read>",
                    "end": "</read>",
                    "children": {
                        "path": {"start": "<path=|", "end": "|>"},
                    }
                },
                "Write": {
                    "start": "<write>",
                    "end": "</write>",
                    "children": {
                        "path": {"start": "<path=|", "end": "|>"},
                        "content": {"start": "<content=|", "end": "|>"},
                    }
                }
            }
        },
        "Tool1": {
            "start": "<tool1>",
            "end": "</tool1>",
            "children": {
                "arg1": {"start": "<arg1=|", "end": "|>"},
                "arg2": {"start": "<arg2=|", "end": "|>"},
            }
        },
        "Tool2": {
            "start": "<tool2>",
            "end": "</tool2>",
            "children": {
                "arg1": {"start": "<arg1=|", "end": "|>"},
                "arg2": {"start": "<arg2=|", "end": "|>"},
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

if __name__ == "__main__":
    test = """
    <tool> 
        <tool1>
            <arg1=|plus1|>
            <arg2=|plus2|>
        </tool1>
    </tool>
    <examples>
        <basic> Whatever </basic>
    </examples>
    """

    parsed = parse_recursive(test, tags)
    print(parsed)