import sys

test_data = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w+')

c = 0
for line in test_data:
  tokens = line.split(' ')
  if tokens[0] == '1':
  	output.write(line)
  else:
  	if c%8 == 0:
  	  output.write(line)
  	  # print c
  	c+=1