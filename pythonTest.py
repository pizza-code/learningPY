from importlib.resources import path
import time
import wmi
import winreg
import platform

conn = wmi.WMI()
# Checks if the type of computer using the Win32_SystemEnclosure WMI class 2 = COMPUTER AND 8 = LAPTOP
type = conn.Win32_SystemEnclosure.chassistypes
with open("FILE.txt", "w") as external_file:
    print(type, file=external_file)
    
#Get the computer time zone
comp_zone = time.tzname
with open("FILE.txt", "w") as external_file:
    print(comp_zone, file=external_file)
    external_file.close()

#Get the running processes (without the thread count)
conn = wmi.WMI()
for process in conn.Win32_Process():
    Proc_id = process.ProcessId
    Proc_name = process.name
    with open("FILE.txt", "w") as external_file:
        print(Proc_id, file=external_file)
        print(Proc_name, file=external_file)
        external_file.close()

#Checks if UAC is enabled using REGISTRY key
key = winreg.OpenKeyEx(path, r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System")
K = "EnableLUA"
value = winreg.QueryValueEx(key, K)            #if value is set to 1 UAC is enabled
with open("FILE.txt", "w") as external_file:
    print(value, file=external_file)
    external_file.close()

#Get the OS version using the platform library
OS_type = platform.system()
OS_build = platform.version()
with open("FILE.txt", "w") as external_file:
    print(OS_type, file=external_file)
    print(OS_build, file=external_file)
    external_file.close()

#Get the OS product key using the Registry key
key = winreg.OpenKeyEx(path, r"Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform")
K = "BackupProductKeyDefault"
value1 = winreg.QueryValueEx(key, K)
with open("FILE.txt", "w") as external_file:
    print(value, file=external_file)
    external_file.close()


    





