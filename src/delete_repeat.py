# python delete_repeat (1)input (2)[output]

import sys

input_file = open(sys.argv[1], 'r')
output_path = sys.argv[2] if len(sys.argv)>2 else sys.argv[1]+'_no_repeat'
output_file = open(output_path, 'w+')

for line in input_file:
  tokens = line.split(' ')
  if int(tokens[0]) < int(tokens[1]):
    output_file.write(line)

