# python separate_back.py (1)origin (2)first out (3)second out

import sys

origin_f = open(sys.argv[1], 'r')
first_f = open(sys.argv[2], 'w')
second_f = open(sys.argv[3], 'w')

for line in origin_f:
  tokens = line.split(' ')
  if tokens[0] == '-1':
    second_f.write(line)
  else:
    first_f.write(line)
