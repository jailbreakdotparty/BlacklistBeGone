import platform
import sys

from sparserestore import backup, perform_restore
from pymobiledevice3.exceptions import NoDeviceConnectedError
from pymobiledevice3.lockdown import create_using_usbmux
import plistlib

def exit(code=0):
    if platform.system() == "Windows" and getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        input("Press Enter to exit...")

    sys.exit(code)

try:
    lockdown = create_using_usbmux()
except NoDeviceConnectedError:
        print("No device connected!")
        print("Please connect your device and try again.")
        exit(1)

def get_nice_ios_version_string():
    os_names = {
        "iPhone": "iOS",
        "iPad": "iPadOS",
        "iPod": "iOS",
        "AppleTV": "tvOS",
        "Watch": "watchOS",
        "AudioAccessory": "HomePod Software Version",
        "RealityDevice": "visionOS",
    }
    device_class = lockdown.get_value(key="DeviceClass")
    product_version = lockdown.get_value(key="ProductVersion")
    os_name = (os_names[device_class] + " " + product_version) if device_class in os_names else ""
    return os_name
    
def menu():
    print(f"""
               BlacklistBeGone v1.1
                by jailbreak.party
          
             Special thanks to Mineek

      Connected to {lockdown.get_value(key="DeviceName")} ({get_nice_ios_version_string()})
        
         === Please select an option. ===
    """)
    print("""
      [1] : Remove Blacklist
            
      [0] : Exit
    """)
    option = None
    try:
        user_input = input("Select an option: ")
        if user_input.strip():
            option = int(float(user_input))
        else:
            input("Please select an option. Press Enter to continue.")
            menu()
    except ValueError:
        input("Please enter a valid number. Press Enter to continue.")
        menu()

    if option is not None:
        if option == 1:
            plist_contents = plistlib.dumps({})
            back = backup.Backup(files=[
                backup.Directory("", "SysContainerDomain-../../../../../../../../var/db/MobileIdentityData/"),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/db/MobileIdentityData/Rejections.plist", contents=plist_contents),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/db/MobileIdentityData/AuthListBannedUpps.plist", contents=plist_contents),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/db/MobileIdentityData/AuthListBannedCdHashes.plist", contents=plist_contents),
                backup.Directory("", "SysContainerDomain-../../../../../../../../var/protected/trustd/private/"),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/protected/trustd/private/ocspcache.sqlite3", contents=b''),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/protected/trustd/private/ocspcache.sqlite3-shm", contents=b''),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../var/protected/trustd/private/ocspcache.sqlite3-wal", contents=b''),
                backup.ConcreteFile("", "SysContainerDomain-../../../../../../../../crash_on_purpose", contents=b'')
            ])
            perform_restore(back, reboot=True)
        elif option == 0:
            print("Thanks for using BlacklistBeGone!")
            exit()
        else:
            input("Please select a valid option. Press Enter to continue.")
            menu()

menu()
