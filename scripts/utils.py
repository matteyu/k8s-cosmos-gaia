import subprocess

"""
Given the file, current line to replace, and the new line, 
this function executes the sed command.
"""
def replace_line_in_file_with_sed(file_path, old_line, new_line):
    try:
        sed_command = f"sed -i'' -e 's/{old_line}/{new_line}/' {file_path}"
        subprocess.run(sed_command, shell=True, check=True)
        # On macOS, the above sed command creates a backup file.  We remove it with this command
        remove_backup_file = f"rm {file_path}-e"
        subprocess.run(remove_backup_file, shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

"""
Given the command this function checks the availability of the program.
"""
def check_command(program_name):
    try:
        result = subprocess.run(
            ["command", "-v", program_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode == 0:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

"""
checks for servicemonitors cdr needed for service monitor resource
"""
def check_service_monitors_crd():
    try:
        # Run the kubectl command to get CRDs and filter with grep
        process = subprocess.Popen(
            ["kubectl", "get", "crds"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Pipe the output of kubectl get crds to grep
        grep_process = subprocess.Popen(
            ["grep", "servicemonitors"],
            stdin=process.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Close the stdout pipe from the first process
        process.stdout.close()

        # Wait for grep process to complete and get the output
        grep_output, _ = grep_process.communicate()

        if grep_output:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

"""
Function to execute commands
"""
def execute_shell(command):
    try:
        # run the Docker command and stream the output to the console
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # stream the stdout and stderr to the console
        for line in process.stdout:
            print(line, end='')
        for line in process.stderr:
            print(line, end='')
        process.wait()
    except Exception as e:
        print(f"An error occurred: {e}")

"""
Given the file path and search string, a function to grep the given file
"""
def get_line_with_grep(file_path, search_pattern):
    try:
        # Construct the grep command to find the line
        grep_command = f"grep '{search_pattern}' {file_path}"

        # Execute the grep command
        result = subprocess.run(grep_command, shell=True,
                                check=True, stdout=subprocess.PIPE, text=True)

        # Get the output which contains the matching line
        output = result.stdout.strip()

        if output:
            return output
        else:
            return

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
