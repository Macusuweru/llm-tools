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

tool_registry = {}
def register_tool(name):
    """Decorator to register tools in the registry"""
    def decorator(func):
        tool_registry[name] = func
        return func
    return decorator

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

def get_args(parsed_dict):
    """Extract arguments from a parsed tool dictionary
    Returns a dictionary of argument names and values"""
    return {k: v for k, v in parsed_dict.items() if k.startswith('arg')}


@register_tool("Tool1")
def tool1(arg1, arg2):
    print("tool1")
    print(arg1)
    print(arg2)
    return

@register_tool("Tool2")
def tool2(arg1, arg2):
    print("tool2")
    print(arg1)
    print(arg2)
    return

"""Memory reading and writing functions for the tool system."""

MEMORY_DIR = os.path.join(os.curdir(), "memory")

@register_tool("MemoryRead")
def memory_read(path):
    """Read content from a file in the memory directory
    
    Args:
        path (str): Relative path within the memory directory
        
    Returns:
        str: Content of the file or None if file doesn't exist
    """
    full_path = os.path.join(MEMORY_DIR, path)
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None

@register_tool("MemoryWrite")
def memory_write(path, content):
    """Write content to a file in the memory directory
    
    Args:
        path (str): Relative path within the memory directory
        content (str): Content to write to the file
    """
    full_path = os.path.join(MEMORY_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w') as f:
        f.write(content)
        
def run_tools(parsed):
    """Execute tools based on parsed input
    parsed: Dictionary from parse_recursive"""
    if "Tools" not in parsed:
        return
        
    for tool_name, tool_content in parsed["Tools"].items():
        print(tool_name)
        print(tool_content)
        if tool_name in tool_registry:
            args = get_args(tool_content)
            tool_registry[tool_name](**args)




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
run_tools(parsed)