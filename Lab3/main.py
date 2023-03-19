import os
import sys
import re
filename = sys.argv[1]
word = sys.argv[2]
text = ""
def process_file (filename, word, count_dict, text):
    count = 0
    f = open(filename, 'r')
    for line in f:
    
        count += line.lower().count(word) 
        if line.startswith('\\input'):
            inner_file = line.split('{')[1].rstrip()[:-1]
            pid = os.fork()
            if pid == 0:
                process_file(inner_file, word, count_dict, text)
                os._exit(0)
            else:
                os.waitpid(pid,0)
        else: 
            text += line
    count_dict[filename] = count
    
    print(count_dict)

count_dict = {}
process_file(filename, word, count_dict, text)
