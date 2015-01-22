# python clean_data.py (1)data_to_be_cleaned (2)output

import sys

input_file = open(sys.argv[1], 'r')
output_file = open(sys.argv[2], 'w+')

# clean data
for line in input_file:
  tokens = line.split(' ')
  tokens = [t[2:] for t in tokens]
  output_file.write(' '.join(tokens[1:]))