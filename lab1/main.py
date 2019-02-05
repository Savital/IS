from installer import TestLicense

def main():
    licenseFlag = TestLicense()

    if licenseFlag == 1:
        print("The license is trusted.")
    elif licenseFlag == 0:
        print("The license isn't trusted.")
    elif licenseFlag == -1:
        print("The platform isn't supported.")
    else:
        print("Error: %d\n", licenseFlag)

    print("Some activity here")


main()

# ubuntu    943d05902e7ed5bdf7276752425d7f43ce3d4ab2712c7398779c110cbad47ec5
# windows   fed275f5a62e68c12e0fac0c2e1ed5dcb7878d4e679224f30004fb27af01b9b4