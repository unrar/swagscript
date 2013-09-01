#!/usr/bin/env python
from os import remove, system
import sys, re

#######################################################################################
#                              SwagScript Suite v1                                    #
#                           SwagScript Compiler (sws) v1                              #
#######################################################################################


### Class: SwsComp
### Description: The compiler itself.

class SwsComp:

    ### Method: __init__
    ### Description: Constructor
    ### Arguments: bool verbose => verbose mode on/off (default is true)
    def __init__(self, verbose=False):
        self.verbose = verbose

    ### Method: open_temp
    ### Description: Open [create] a temporary file where the compiled Python code will be written.
    ### Arguments: none
    def open_temp(self):
        try:
            # Create the file
            f = open("swstemp.py", 'w')
        except OSError:
            print("    [ERROR] Error while creating the temporary file. Aborting...")
            return False
        else:
            # If verbose mode:
            if self.verbose: print("    [INFO] Temporary file %s properly created." % "swstemp.py")
            return f

    ### Method: close_temp
    ### Description: Close and delete the temporary file while the Python code was written.
    ### Arguments: File file => Was returned by open_temp (see above)
    def close_temp(self, file):
        try:
            # Close the file
            #file.close()
            remove(file.name)
        except OSError:
            print("    [ERROR] Error while closing and deleting the temporary file. Aborting...")
            return False
        else:
            # If verbose mode:
            if self.verbose: print("    [INFO] Temporary file %s properly closed and removed." % file.name)
            return True

    ### Method: open_sws
    ### Description: Open the .sws file with the SwagScript code.
    ### Arguments: filename
    def open_sws(self, filename):
        try:
            # Open file in read mode
            f = open(filename, 'r')
        except OSError:
            print("    [ERROR] Error while opening the SwagScript file. Aborting...")
            return False
        else:
            #If verbose:
            if self.verbose: print("    [INFO] Properly opened the SwagScript file %s!" % filename)
            return f

    ### Method: close_sws
    ### Description: Close the .sws file provided.
    ### Arguments: File file
    def close_sws(self, file):
        try:
            file.close()
        except OSError:
            print("    [ERROR] Error while closing the SwagScript file %s. Aborting..." % file.name)
            return False
        else:
            # If verbose
            if self.verbose: print("    [INFO] Properly closed the SwagScript file %s." % file.name)
            return True

    ### Method: parse_file
    ### Description: Parseas each line of swsfile and writes it to tmpfile.
    ### Arguments: swspath => path of the SwagScript file
    def parse_file(self, swspath):
        if self.verbose: print("[INFO] Started parsing file process. Trying to open SwagScript file %s..." % swspath)
        # Open it
        swsfile = self.open_sws(swspath)
        if not swsfile:
            # Exit program
            exit(1)

        # Open the temp file
        if self.verbose: print("[INFO] Trying to open the temporary Python file...")
        tmpfile = self.open_temp()
        if not tmpfile:
            # Exit program
            exit(1)

        # Read each line of swsfile
        for line in swsfile.readlines():
            # Process line
            pline = self.parse_line(line)
            tmpfile.write(pline + '\n')

        # We have it! Close SwagScript now
        self.close_sws(swsfile)

        # Get the name without extension
        trs = re.search(r"^(.+)\.py$", tmpfile.name)
        print(trs.group(1))
        onlyname = trs.group(1)
        tmpfile.close()
        # Run tmpfile
        exec("import " + onlyname)

        # Done! Remove tmpfile
        self.close_temp(tmpfile)

    ### Method: parse_line
    ### Description: Convert a line from SwagScript to Python
    ### Arguments: line

    def parse_line(self, line):
        #
        # This is the core of sws.
        # Some useful tips:
        #  * ATM, lines are parsed one-at-time, the "context" doesn't matter. That means that SwagScript use the same
        #    indentation rules as Python, so it doesn't matter if a line is at the beggining of the file, after an
        #    if or after three nested for loops!
        #  * To add a new conversion, just add a new entry to possible and an elif.
        #  * Do __NOT__ add [\r]\n at the end of a line, it's added by parse_file!
        #  * Knowledge of basic-medium regex is mandatory! If you don't do regex, don't keep reeding! ;)

        # Remove [\r]\n
        line = line.rstrip()

        # Dictionary of possible matches
        possible = {"yo": re.search(r"^yo(.*)$", line, re.IGNORECASE),
                    "gimme": re.search(r"^gimme (.+) bro$", line, re.IGNORECASE),
                    "hai": re.search(r"^hai$", line, re.IGNORECASE)
                    }
        if possible["yo"] and not possible["yo"].group(1):
            return "#!/usr/bin/env python"
        elif possible["yo"] and possible["yo"].group(1):
            return "#!/usr/bin/env python\n#Program " + possible["yo"].group(1)
        elif possible["gimme"]:
            return "import " + possible["gimme"].group(1)
        elif possible["hai"]:
            return "print(\"Hai homie yo!\")"
        else:
            return line


