#! /usr/bin/env python

import re
import sys
import string
import array

DoFindConf = True
DoFindLines = True
DoFindRate = True

# Define the logfiles you want to compare
logfiles = ['trial.log'
            ]

# Define the lines you are interested in
relines = ["Hlt1SingleMuonNoIP",
           "Hlt1SingleMuonIP",
           "Hlt1MuonPrep",
           "Hlt1DiMuon"
           ]

# ------------ FUNCTIONS --------------

def FindConf(line):
    m = re.search("(Using trigger threshold settings \")(.+)(\" )",line)
    if m:
        print "# ------------------------------------------------------------ #"
        print "# Configuration file: ", m.group(2)
        print "# ------------------------------------------------------------ #"
        return True
    else:
        return False
    
##         while not EOF(line):
##             if FindConf(line):
##                 print FindConf(line)
##                 break
##             else:
##                 line = f.readline()

def FindLines(line):
    global relines
    result = False
    # Find trigger lines of interest and parse their contents
    for regex in relines:
        m = re.search("(^" + regex + "[a-zA-Z0-9]+)",line)
        if m and re.search("SUCCESS",line):
            result =  m.group(0) # If we get a match print the whole line
            break # No need to parse the rest of the regexpressions
    return result

def FindAccept(line):
    m = re.search("(\#accept\"\s+)(.+)(-------   \|   ------)",line)
    if m:
        return m.group(2)
    else:
        return False

def EOF(line):
    # Break if EOF
    if len(line) == 0:
        return True
    else:
        return False
    
def main():
    global logfiles
    for file in logfiles:
        print "Opening file: ", file
        
        f = open(file, 'r')

        line = f.readline() 

        if DoFindConf:
            while not FindConf(line):
                line = f.readline()

        if DoFindLines:
            while not EOF(line):
                if FindLines(line):
                    LineName = FindLines(line)
                    f.readline() # Skip a line
                    while not EOF(line):
                        if not FindAccept(line):
                            line = f.readline()
                        else:
                            space = 35-len(LineName)
                            TheLine = LineName + " " * space + FindAccept(line)
                            print TheLine
                            if DoFindRate:
                                m = re.search("(\w+)PostScaler\s+\|\s+(\d+)\s\|\s+(\d+)\s\|",TheLine)
                                if m:
                                    print "----------------------------------------------------"
                                    print "Frequency for line: ", m.group(1), " = ", m.group(3)
                                    print "----------------------------------------------------\n"
                            break

                line = f.readline()

if __name__ == "__main__":
    main()
