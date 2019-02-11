from sys import platform
from subprocess import check_output
import hashlib

def GetSum():
    if platform == "win32":
        hardUUID = check_output("wmic csproduct get UUID", shell=True).decode()
        serialNum = check_output("wmic baseboard get serialnumber", shell=True).decode()
    else:
        return ""
    sumStr = hardUUID + " " + serialNum
    return hashlib.sha256(sumStr.encode('utf-8')).hexdigest()

def VerifySum():
    real_key = GetLicense()
    sum = GetSum()

    if (sum == ""):
        return -1
    if (real_key == sum):
        return 1
    return 0

def SetLicense(checksum):
    with open("license.key", "w") as license_file:
        license_file.write((checksum))

def GetLicense():
    with open("license.key", "r") as license_file:
        return license_file.readline()

def TestLicense():
    #print(GetSum())
    #print(GetLicense())
    return VerifySum()
