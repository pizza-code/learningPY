import os
import winreg
import platform
import subprocess

def create_hidden_directory_and_file(directory, filename):
    # Create the hidden directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    subprocess.run(['attrib', '+h', directory])  # Set the directory as hidden

    # Create the file within the hidden directory
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        open(filepath, "w").close()  # Create an empty file

    return filepath

def write_to_file(filepath, *contents):
    with open(filepath, "a") as file:
        file.writelines(str(content) + "\n" for content in contents)

def get_running_processes():
    output = subprocess.run(['tasklist', '/fo', 'csv'], capture_output=True, text=True).stdout
    processes = output.strip().splitlines()[1:]
    return [process.split(",", maxsplit=1) for process in processes]

def is_uac_enabled():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        enable_lua_value = winreg.QueryValueEx(key, "EnableLUA")[0]
        return enable_lua_value == 1
    except FileNotFoundError:
        return False

def main():
    # Specify the hidden directory and file name
    hidden_directory = ".hidden"
    filename = "FILE.txt"

    # Create the hidden directory and file
    filepath = create_hidden_directory_and_file(hidden_directory, filename)

    # Write system information to the file
    write_to_file(filepath, "Computer Type:", platform.machine())
    write_to_file(filepath, "Computer Time Zone:", platform.timezone())
    write_to_file(filepath, "Running Processes:")
    for process_id, process_name in get_running_processes():
        write_to_file(filepath, process_id.strip('"'), process_name.strip('"'))
    write_to_file(filepath, "UAC Enabled:", "Yes" if is_uac_enabled() else "No")
    write_to_file(filepath, "OS Type:", platform.system())
    write_to_file(filepath, "OS Version:", platform.release())

    # Get the OS product key
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform")
        product_key = winreg.QueryValueEx(key, "BackupProductKeyDefault")[0]
        write_to_file(filepath, "Product Key:", product_key)
    except FileNotFoundError:
        write_to_file(filepath, "Product Key: Not Found")

if __name__ == "__main__":
    main()