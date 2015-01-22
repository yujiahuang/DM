# python gen_feature.py (1)past_data (2)ans_data (3)data_to_be_processed (4)[output]

import sys

# open input
input_file = open(sys.argv[3], 'r')

# open output
output_path = sys.argv[4] if len(sys.argv)>4 else './data/feature_data'
output_file = open(output_path, 'w+')

# open reference data
past_data = open(sys.argv[1], 'r')
ans_data = open(sys.argv[2], 'r') if len(sys.argv)>2 and sys.argv[2]!='None' else None


def get_label(author1, author2):

  for line in ans_data:
    tokens = line.split(' ')
    if (author1, author2) == (tokens[0], tokens[1]):
      return '+1'
  ans_data.seek(0) # rewind
  return '-1'

def count_coop_times(author1, author2):
  if int(author1) > int(author2):
    author1, author2 = author2, author1

  count = 0
  for line in past_data:
    tokens = line.split(' ')
    print author1, author2, tokens[0], tokens[1]
    
    if (author1, author2) == (tokens[0], tokens[1]):
      count+=1

  past_data.seek(0) # rewind
  return count

# helper


def main():

  for line in input_file:

    # print 'line: ' + line
    tokens = line.split(' ')
    print 'tokens: {0}\n'.format(tokens)

    # gen feature
    label = get_label(tokens[0], tokens[1]) if ans_data else 0
    coop_times = count_coop_times(tokens[0], tokens[1])
    output_file.write('{0} 1:{1}\n'.format(label, coop_times))

main()

