# python trans_data dataset year_as_test

import sys

input_file = open(sys.argv[1], 'r')
past_data = open('./data/past_data', 'w+')
_temp_past_data = open('./data/_temp_past_data', 'w+')
ans_data = open('./data/ans_data', 'w+')

year_as_test = sys.argv[2]


for line in input_file:
  tokens = line.split(' ')
  if tokens[2] != year_as_test:
    for i, t in enumerate(tokens):
      tokens[i] = ' {0}:{1}'.format(i+1 ,t)
    _temp_past_data.write(tokens[2][3:] + ''.join(tokens));
    past_data.write(line);
  else:
    ans_data.write(line);


