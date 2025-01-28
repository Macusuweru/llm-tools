import os
from parse import parse_recursive


tool_registry = {}
def register_tool(name):
    """Decorator to register tools in the registry"""
    def decorator(func):
        tool_registry[name] = func
        return func
    return decorator



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