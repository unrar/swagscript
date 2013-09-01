import sws, sys

# Check arguments
if len(sys.argv) < 2:
    print("Syntax error! Correct usage: python ssc.py file.sws [--verbose]")
    exit(1)
# Init swag
swag = ""
if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
    swag = sws.SwsComp(True)
else:
    swag = sws.SwsComp()

# Parse file
swag.parse_file(sys.argv[1])