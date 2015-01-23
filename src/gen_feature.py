# python gen_feature.py (1)past_data (2)ans_data (3)data_to_be_processed (4)[output]

import sys
from collections import OrderedDict
import networkx as nx

# open input
input_file = open(sys.argv[3], 'r')

# open output
output_path = sys.argv[4] if len(sys.argv)>4 else './data/feature_data'
output_file = open(output_path, 'w+')

# open reference data
past_data = open(sys.argv[1], 'r')
ans_data = open(sys.argv[2], 'r') if len(sys.argv)>2 and sys.argv[2]!='None' else None

# hetero_graph takes author and conference as nodes, whereas homo_graph only take author
hetero_graph = nx.Graph()
homo_graph = nx.Graph()

# generate features
def get_label(author1, author2):
  for line in ans_data:
    tokens = line.split(' ')
    if (author1, author2) == (tokens[0], tokens[1]):
      return '+1'
  ans_data.seek(0) # rewind
  return '-1'

def gen_features(author1, author2):
  # Pi = Publications of i, CRi = collaborators of i, CNi = collaborations of i
  # here CN12 = P12
  P1, P2, P12, CR1, CR2, CN1, CN2 = [], [] ,[], [], [], [], []
  # 3 ways of representing last publication year: linear, quadratic, and exponential
  # [author1, author2, cooperation]
  last_pub_year_lin = [0, 0, 0]
  last_pub_year_qua = [0, 0, 0]
  last_pub_year_exp = [0, 0, 0]
  # a dictionary recording author1 and author2 in the same conference
  same_conf = {}

  for line in past_data:
    tokens = line.split(' ')
    paper_id = tokens[2] + ' ' + tokens[3] + ' ' + tokens[4]

    # compare match
    if tokens[0] == author1:
      P1.append(paper_id)
      CR1.append(tokens[1])
      CN1.append(tokens[1] + ' ' + paper_id)
      last_pub_year_lin[0] = int(tokens[2]) - 2007
      last_pub_year_qua[0] = (int(tokens[2]) - 2007)**2
      last_pub_year_exp[0] = 2**(int(tokens[2]) - 2007)
    if tokens[1] == author2:
      P2.append(paper_id)
      CR2.append(tokens[0])
      CN2.append(tokens[0] + ' ' + paper_id)
      last_pub_year_lin[1] = int(tokens[2]) - 2007
      last_pub_year_qua[1] = (int(tokens[2]) - 2007)**2
      last_pub_year_exp[1] = 2**(int(tokens[2]) - 2007)
    if (author1, author2) == (tokens[0], tokens[1]):
      P12.append(paper_id)
      last_pub_year_lin[2] = int(tokens[2]) - 2007
      last_pub_year_qua[2] = (int(tokens[2]) - 2007)**2
      last_pub_year_exp[2] = 2**(int(tokens[2]) - 2007)
      if tokens[3] in same_conf:
        same_conf[tokens[3]] += 1
      else:
        same_conf[tokens[3]] = 1
  
  # rewind
  past_data.seek(0)

  # make unique
  P1 = list(OrderedDict.fromkeys(P1))
  P2 = list(OrderedDict.fromkeys(P2))
  CR1 = list(OrderedDict.fromkeys(CR1))
  CR2 = list(OrderedDict.fromkeys(CR2))
  CN1 = list(OrderedDict.fromkeys(CN1))
  CN2 = list(OrderedDict.fromkeys(CN2))

  # calc features
  first_co_ratio1 = float(len(P12))/float(len(P1))
  first_co_ratio2 = float(len(P12))/float(len(P2))
  first_co_ratio12 = float(len(P12))/float(len(P1) + len(P2))
  second_co_ratio1 = float(len(P12))/float(len(CN1))
  second_co_ratio2 = float(len(P12))/float(len(CN2))
  second_co_ratio12 = float(len(P12))/float(len(CN1) + len(CN2))
  third_co_ratio1 = 1.0/float(len(CR1))
  third_co_ratio2 = 1.0/float(len(CR2))
  num_same_conf = max(same_conf.values())
  
  # weighted count
  P12_weighted = 0
  for c in P12:
    P12_weighted += ( int( c[0:c.find(' ')] ) - 2007 )

  # degrees features
  try:
    hetero_degrees = nx.shortest_path_length(hetero_graph, 'author'+author1, 'author'+author2)
  except nx.NetworkXNoPath:
    hetero_degrees = 999999
  try:
    homo_degrees = nx.shortest_path_length(homo_graph, 'author'+author1, 'author'+author2)
  except nx.NetworkXNoPath:
    homo_degrees = 999999

  features = (
              len(P1), len(P2), len(CR1), len(CR2), len(CN1), len(CN2), 
              last_pub_year_lin[0], last_pub_year_qua[0], last_pub_year_exp[0], 
              last_pub_year_lin[1], last_pub_year_qua[1], last_pub_year_exp[1], 
              len(P12), P12_weighted, first_co_ratio1, first_co_ratio2, first_co_ratio12, 
              second_co_ratio1, second_co_ratio2, second_co_ratio12,
              third_co_ratio1, third_co_ratio2, 
              last_pub_year_lin[2], last_pub_year_qua[2], last_pub_year_exp[2],
              num_same_conf
              # , hetero_degrees, homo_degrees
              )
  return features

def createGraphs():
  for line in past_data: 
    tokens = line.split(' ')
    hetero_graph.add_edge('author'+tokens[0], 'conf'+tokens[3])
    hetero_graph.add_edge('author'+tokens[1], 'conf'+tokens[3])
    homo_graph.add_edge('author'+tokens[0], 'author'+tokens[1])
  past_data.seek(0)
  print nx.shortest_path_length(hetero_graph, 'author202', 'author203')

# helper

def getAuthorPairs():
  author_pairs = []
  for line in input_file:
    tokens = line.split(' ')
    author_pairs.append((tokens[0], tokens[1]))
  input_file.seek(0)
  return list(OrderedDict.fromkeys(author_pairs))


# main
def main():

  createGraphs()

  author_pairs = getAuthorPairs()
  for ap in author_pairs:
    label = get_label(ap[0], ap[1]) if ans_data else 0
    features = gen_features(ap[0], ap[1])

    output_file.write(label)
    for i, f in enumerate(features):
      output_file.write(' {0}:{1}'.format(i+1, f))
    output_file.write('\n')



  # for line in input_file:

  #   tokens = line.split(' ')

  #   repeated = False
  #   output_file.seek(0)
  #   for written_line in output_file:
  #     written_tokens = written_line.split(' ')
  #     written_a1 = written_tokens[1][2:]
  #     written_a2 = written_tokens[2][2:]
  #     if (written_a1, written_a2) == (tokens[0], tokens[1]):
  #       repeated = True
  #       output_file.seek(0, 2) # move to the end

  #   # gen feature
  #   if not repeated:
  #     label = get_label(tokens[0], tokens[1]) if ans_data else 0
  #     features = gen_features(tokens[0], tokens[1])

  #     output_file.write(label)
  #     for i, f in enumerate(features):
  #       output_file.write(' {0}:{1}'.format(i+1, f))
  #     output_file.write('\n')
      

main()

