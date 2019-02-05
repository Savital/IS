from installer import GetSum
from installer import SetLicense

checkSum = GetSum()
SetLicense(checkSum)

print("New license is: {", checkSum, "}\n")