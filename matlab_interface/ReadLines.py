import os
from time import sleep
num_of_lines = 0;
with open('send.txt', 'r') as f:
    data = f.readlines()
data = [x.strip() for x in data]
num_of_lines = len(data);
lines = num_of_lines;
while lines == num_of_lines:
    with open('send.txt', 'r') as f:
        data = f.readlines()
    data = [x.strip() for x in data]
    num_of_lines = len(data);
    sleep(2)
print ("Got new lines")
#os.popen("cat send.txt | nc 192.168.1.110 2999")
