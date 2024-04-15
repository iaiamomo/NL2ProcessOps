import re

if __name__ == "__main__":
    py_code = "p02"
    py_code = f"f/{py_code}/{py_code}_code_r"

    script_content = open(f"{py_code}.py", "r").read()

    # Define the modification rules using regular expressions
    modification_rules = [
        # call -> fake_call
        (r'\.call\(.*\)', r'.fake_call()'),
        # condition in quotes
        (r'beautiful_pipeline_check\((.*)\)', r'beautiful_pipeline_check("\1")'),
        # loop condition in quotes
        (r'beautiful_pipeline_loop_check\((.*)\)', r'beautiful_pipeline_loop_check("\1", loop_count)'),
        # else -> elif
        (r'else', r'elif beautiful_pipeline_check("otherwise")'),
        # continue -> beautiful_pipeline_continue()
        (r'continue', r'beautiful_pipeline_continue()'),
        # break -> beautiful_pipeline_break()
        (r'break', r'beautiful_pipeline_break()'),
    ]

    # Apply modification rules
    for pattern, replacement in modification_rules:
        script_content = re.sub(pattern, replacement, script_content)

    beautiful_pipeline_def = open("tools/beautiful_pipeline.py", "r").read()
    # Add continue and break statements
    new_script_content = ""
    new_script_content += beautiful_pipeline_def + "\n"
    new_script_content += "loop_count = 0\n"
    for line in script_content.split("\n"):
        new_script_content += line + "\n"
        if "beautiful_pipeline_continue()" in line:
            if line.strip():
                indent_count = len(line) - len(line.lstrip())
                new_script_content += f"{' ' * indent_count}continue\n"
            else:
                new_script_content += "continue\n"
        elif "beautiful_pipeline_break()" in line:
            if line.strip():
                indent_count = len(line) - len(line.lstrip())
                new_script_content += f"{' ' * indent_count}break\n"
            else:
                new_script_content += "break\n"

    print(new_script_content)

    # Write the modified script to a new file
    with open(f"{py_code}_modified.py", "w") as f:
        f.write(new_script_content)
