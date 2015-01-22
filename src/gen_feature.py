# python gen_feature.py (1)past_data (2)ans_data (3)data_to_be_processed (4)[output]

import sys
from collections import OrderedDict

# open input
input_file = open(sys.argv[3], 'r')

# open output
output_path = sys.argv[4] if len(sys.argv)>4 else './data/feature_data'
output_file = open(output_path, 'w+')

# open reference data
past_data = open(sys.argv[1], 'r')
ans_data = open(sys.argv[2], 'r') if len(sys.argv)>2 and sys.argv[2]!='None' else None

# generate features
def get_label(author1, author2):
  for line in ans_data:
    tokens = line.split(' ')
    if (author1, author2) == (tokens[0], tokens[1]):
      return '+1'
  ans_data.seek(0) # rewind
  return '-1'

def gen_features(author1, author2):
  total1 = []
  total2 = []
  coop = []
  for line in past_data:
    tokens = line.split(' ')
    paper_id = tokens[2] + ' ' + tokens[3] + ' ' + tokens[4]
    if (author1, author2) == (tokens[0], tokens[1]):
      coop.append(paper_id)
      total1.append(paper_id)
      total2.append(paper_id)
    elif tokens[0] == author1:
      total1.append(paper_id)
    elif tokens[1] == author2:
      total2.append(paper_id)
  
  # rewind
  past_data.seek(0)

  # make unique
  total1 = list(OrderedDict.fromkeys(total1))
  total2 = list(OrderedDict.fromkeys(total2))
  # coop = list(OrderedDict.fromkeys(coop))

  # features
  coop_ratio1 = float(len(coop))/float(len(total1))
  coop_ratio2 = float(len(coop))/float(len(total2))
  count = len(coop)
  score = 0
  for c in coop:
    score += ( int( c[0:c.find(' ')] ) - 2007 )

  return count, score, coop_ratio1, coop_ratio2

# helper

# main
def main():

  for line in input_file:

    tokens = line.split(' ')

    repeated = False
    output_file.seek(0)
    for written_line in output_file:
      written_tokens = written_line.split(' ')
      written_a1 = written_tokens[1][2:]
      written_a2 = written_tokens[2][2:]
      if (written_a1, written_a2) == (tokens[0], tokens[1]):
        repeated = True
        output_file.seek(0, 2) # move to the end

    # gen feature
    if not repeated:
      label = get_label(tokens[0], tokens[1]) if ans_data else 0
      coop_times, weighted_coop, coop_ratio1, coop_ratio2 = gen_features(tokens[0], tokens[1])
      output_file.write('{0} 1:{1} 2:{2} 3:{3} 4:{4} 5:{5} 6:{6}\n'
        .format(label, tokens[0], tokens[1], coop_times, weighted_coop, coop_ratio1, coop_ratio2))

main()

