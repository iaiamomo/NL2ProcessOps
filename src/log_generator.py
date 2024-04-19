import re
import subprocess

def script_log_generator(script_content, tool_reference):
    # Define the modification rules using regular expressions
    modification_rules = [
        # call -> fake_call
        (r'(?:(\w+.*) = )?(\w+)\.call\(.*\)', r'\2.fake_call()'),
        # call in thread -> fake_call in thread
        (r'threading\.Thread\(target=(\w+)\.call(?:, args=\(.*\))?\)', r'threading.Thread(target=\1.fake_call)'),
        # remove parameters in function definition
        (r'def (\w+)\(.*\):', r'def \1():'),
        # return -> return True
        (r'return (.*(?!True|False))', r'return True'),
        # call in thread without args
        (r'threading\.Thread\(target=(\w+).*\)', r'threading.Thread(target=\1)'),
        # whatever function call without args
        (r'(?:\w+.*)? = (\w+(?!threading.Thread))\(.*\)', r'\1()'),
        # condition in quotes
        (r'beautiful_pipeline_check\((.*)\)', r"beautiful_pipeline_check('\1')"),
        # loop condition in quotes
        (r'beautiful_pipeline_loop_check\((.*)\)', r"beautiful_pipeline_loop_check('\1')"),
        # else -> if
        (r'else', r"if beautiful_pipeline_check('otherwise')"),
        # elif -> if
        (r'elif beautiful_pipeline_check', r"if beautiful_pipeline_check_elif"),
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
    new_script_content += "import sys\n"
    new_script_content += f"sys.path.append('{tool_reference}')\n"
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

    #print(new_script_content)
    return new_script_content


def run_script(p_id, script, folder_files):
    with open(f"{folder_files}/{p_id}/output_{p_id}.txt", "w+") as output:
        subprocess.call(["python", f"{script}.py"], stdout=output)
        print(f"Script {script} executed successfully!")


if __name__ == "__main__":

    folder_files = "f_new"

    for i in range(1, 11):
        proc_id = f"p0{i}" if i < 10 else "p10"

        py_code_log = f"{folder_files}/{proc_id}/{proc_id}_code_r_modified"
        run_script(proc_id, py_code_log, folder_files)

        py_code = f"{folder_files}/{proc_id}/{proc_id}_code_r"
        script_content = open(f"{py_code}.py", "r").read()
        new_script_content = script_log_generator(script_content, './')
        # Write the modified script to a new file
        f = open(f"{py_code}_modified.py", "r")
        #f.write(new_script_content)
        f.close()
