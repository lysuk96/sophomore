import sys
import os
import subprocess as proc
import re

if (len(sys.argv) <= 1):
    print ("Usage: ./gitv [Keyword]")
    exit()

cmdLine = "git ls-files `git rev-parse --show-toplevel`"
pipeFile = proc.Popen(cmdLine, shell = True, stdout = proc.PIPE)

childOutput = pipeFile.stdout.readlines()
done = False
word = re.compile(sys.argv[1])

while (done == False):
    applicants = []
    count = 0
    for line in childOutput:
        if((count < 10) and (word.search(line.split('/')[-1]) != None)):
            applicants.append(line.rstrip())
            count += 1
        childOutput = applicants

    if (count == 0):
        print "there's no such element."
        done = True
    elif (count == 1):
        proc.call(["vi",applicants[0]])
        done=True
    else :
        while 1:
            for i in range (0, len(applicants)) :
                print(applicants[i] + ' (' + str(i+1) + ')')

            #choose or refine files
            instruction = raw_input("Enter file shortcut (shown on the right) or keyword to further refine the search:\n")

            if (instruction.isdigit() and int(instruction) > 0 and int (instruction) < 11):
                proc.call(["vi", applicants[int(instruction) - 1]])
                break
            else :
                tmp = []
                tmp_word = re.compile(instruction)

                for filename in applicants:
                    if (tmp_word.search(filename.split('/')[-1]) != None):
                        tmp.append(filename)
                applicants = tmp

            if len(applicants) == 0 :
                print "there's no such element."
                done = True
                break
            elif len(applicants) == 1 :
                proc.call(["vi",applicants[0]])
                done = True
                break
