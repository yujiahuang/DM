# python gen_feature.py (1)past_data (2)ans_data (3)data_to_be_processed (4)output 
# (5)[is_all=1, is_feature=-1]

import sys
from collections import OrderedDict
# import networkx as nx

def is_2013():
  return (len(sys.argv)>5 and sys.argv[5]=='-1')

# open input
input_file = open(sys.argv[3], 'r')

# open output
output_file = open(sys.argv[4], 'w+')

# open reference data
past_data = open(sys.argv[1], 'r')
ans_data = open(sys.argv[2], 'r') if sys.argv[2]!='None' else None

last_year = 2012 if is_2013() else 2011
# generate features

# author_hash has key the author id and value in the following format:
# [ P[...], CR[...], CN[...] ]
# co_hash has key the author pair and value co_papers
author_hash = {}
co_hash = {}
ans_hash = {}
def createHash():
  for line in past_data:
    tokens = line.split(' ')

    paper_id = 'year' + tokens[2] + ' conf' + tokens[3] + ' paper'+tokens[4]

    # gen author hash
    for i in [0, 1]:
      j = 1 if i==0 else 0
      collaboration = 'author' + tokens[j] + ' ' + paper_id
      if tokens[i] in author_hash:
        P = author_hash[tokens[i]][0]
        CR = author_hash[tokens[i]][1]
        CN = author_hash[tokens[i]][2]
        if paper_id not in P: author_hash[tokens[i]][0].append(paper_id)
        if tokens[j] not in CR: author_hash[tokens[i]][1].append(tokens[j])
        if collaboration not in CN: author_hash[tokens[i]][2].append(collaboration)
      else:
        author_hash[tokens[i]] = [ [], [], [] ]
        author_hash[tokens[i]][0].append(paper_id)
        author_hash[tokens[i]][1].append(tokens[j])
        author_hash[tokens[i]][2].append(collaboration)

    # gen co hash
    if (tokens[0], tokens[1]) in co_hash:
      co_papers = co_hash[(tokens[0], tokens[1])]
      if paper_id not in co_papers: co_hash[(tokens[0], tokens[1])].append(paper_id)
    else:
      co_hash[(tokens[0], tokens[1])] = [ paper_id ]

  past_data.seek(0)

  if not is_2013():
    # gen ans hash
    for line in ans_data:
      tokens = line.split(' ')
      ans_hash[ (tokens[0], tokens[1]) ] = 1
    ans_data.seek(0)

# generate features
def get_label(author1, author2):
  # 1: cowork again, 0: not, -1: don't know
  if (author1, author2) in ans_hash:
    return '1'
  else:
    return '0'

def gen_features(author_pair):
  P = [[],[]]
  P[0] = author_hash[author_pair[0]][0]
  P[1] = author_hash[author_pair[1]][0]

  CR = [[],[]]
  CR[0] = author_hash[author_pair[0]][1]
  CR[1] = author_hash[author_pair[1]][1]

  co_papers = co_hash[author_pair]

  CN = [[],[]]
  CN[0] = author_hash[author_pair[0]][2]
  CN[1] = author_hash[author_pair[1]][2]

  # gen weighted paper sum
  weighted_lin = [0, 0, 0]
  weighted_qua = [0, 0, 0]
  weighted_exp = [0, 0, 0]
  for i in [0, 1]:
    for paper in P[i]:
      paper_attr = paper.split(' ')
      weighted_lin[i] += int(paper_attr[0][4:])-2007
      weighted_qua[i] += (int(paper_attr[0][4:])-2007)**2
      weighted_exp[i] += 2**(int(paper_attr[0][4:])-2007)
  for paper in co_papers:
    paper_attr = paper.split(' ')
    weighted_lin[2] += int(paper_attr[0][4:])-2007
    weighted_qua[2] += (int(paper_attr[0][4:])-2007)**2
    weighted_exp[2] += 2**(int(paper_attr[0][4:])-2007)

  # basic counts
  P_count = [ len(P[0]), 
              len(P[1]),
              len(co_papers) ]
  CR_count = [len(CR[0]), 
              len(CR[1]),
              len(set(CR[0]) & set(CR[1])) ]
  CN_count = [len(CN[0]), 
              len(CN[1]),]

  # publication count each year and whether collaboration each year
  # [2008, 2009, 2010, 2011] or [2009, 2010, 2011, 2012] for 2013
  Y = [ [0, 0, 0, 0], [0, 0, 0, 0] ]
  Y12 = [0, 0, 0, 0]
  Y_binary = [ [0, 0, 0, 0], [0, 0, 0, 0] ]
  Y12_binary = [0, 0, 0, 0]

  bias = 2009 if is_2013() else 2008

  for i in [0, 1]:
    for p in P[i]:
      p_attr = p.split(' ')
      idx = int(p_attr[0][4:])-bias
      Y[i][idx] += 1
      Y_binary[i][idx] = 1
  for p in co_papers:
    p_attr = p.split(' ')
    idx = int(p_attr[0][4:])-bias
    Y12[idx] += 1
    Y12_binary[idx] = 1

  # conference
  CONF = [ {}, {}, {} ]
  for i in [0, 1]:
    for p in P[i]:
      p_attr = p.split(' ')
      c = p_attr[1]
      if c in CONF[i]:
        CONF[i][c] += 1
      else:
        CONF[i][c] = 1
  for paper in co_papers:
    paper_attr = paper.split(' ')
    if paper_attr[1] in CONF[2]:
      CONF[2][paper_attr[1]] += 1
    else:
      CONF[2][paper_attr[1]] = 1

  CONF_count = [ len(CONF[0].keys()), len(CONF[1].keys()), len( CONF[2].keys() ) ]
  num_same_conf = max(CONF[2].values())

  # co ratios
  first_co_ratio1 = float(P_count[2])/float(P_count[0])
  first_co_ratio2 = float(P_count[2])/float(P_count[1])
  first_co_ratio12 = float(P_count[2])/float(P_count[0] + P_count[1])

  second_co_ratio1 = float(P_count[2])/float(CN_count[0])
  second_co_ratio2 = float(P_count[2])/float(CN_count[1])
  second_co_ratio12 = float(P_count[2])/float(CN_count[0] + CN_count[1])
  
  third_co_ratio1 = float(CR_count[2])/float(CR_count[0])
  third_co_ratio2 = float(CR_count[2])/float(CR_count[1])
  third_co_ratio12 = float(CR_count[2])/float(CR_count[0] + CR_count[1])
  
  forth_co_ratio1 = 1/float(CR_count[0])
  forth_co_ratio2 = 1/float(CR_count[1])
  forth_co_ratio12 = 1/float(CR_count[0] + CR_count[1])
  
  fifth_co_ratio1 = float(weighted_lin[2])/float(weighted_lin[0])
  fifth_co_ratio2 = float(weighted_lin[2])/float(weighted_lin[1])
  fifth_co_ratio12 = float(weighted_lin[2])/float(weighted_lin[0] + weighted_lin[1])
  
  sixth_co_ratio1 = float(weighted_qua[2])/float(weighted_qua[0])
  sixth_co_ratio2 = float(weighted_qua[2])/float(weighted_qua[1])
  sixth_co_ratio12 = float(weighted_qua[2])/float(weighted_qua[0] + weighted_qua[1])
  
  seventh_co_ratio1 = float(weighted_exp[2])/float(weighted_exp[0])
  seventh_co_ratio2 = float(weighted_exp[2])/float(weighted_exp[1])
  seventh_co_ratio12 = float(weighted_exp[2])/float(weighted_exp[0] + weighted_exp[1])
  
  eighth_co_ratio1 = float(CONF_count[2])/float(CONF_count[0])
  eighth_co_ratio2 = float(CONF_count[2])/float(CONF_count[1])
  eighth_co_ratio12 = float(CONF_count[2])/float(CONF_count[0] + CONF_count[1])
    
  # last publication year
  last_pub_year_lin = [0, 0, 0]
  last_pub_year_qua = [0, 0, 0]
  last_pub_year_exp = [0, 0, 0]
  for i in [0, 1]:
    for paper in P[i]:
      paper_attr = paper.split(' ')
      new_year = int(paper_attr[0][4:])-2007
      old_year = int(last_pub_year_lin[i])
      if new_year > old_year:
        last_pub_year_lin[i] = new_year
        last_pub_year_qua[i] = new_year**2
        last_pub_year_exp[i] = 2**new_year

  for path in co_papers:
    paper_attr = paper.split(' ')
    new_year = int(paper_attr[0][4:])-2007
    old_year = int(last_pub_year_lin[2])
    if new_year > old_year:
      last_pub_year_lin[2] = new_year
      last_pub_year_qua[2] = new_year**2
      last_pub_year_exp[2] = 2**new_year


  # all features
  features = (
              P_count[0], P_count[1], CR_count[0], 
              CR_count[1], CN_count[0], CN_count[1], 
              weighted_lin[0], weighted_lin[1], weighted_qua[0], 
              weighted_qua[1], last_pub_year_lin[0], last_pub_year_qua[0], 
              last_pub_year_exp[0], last_pub_year_lin[1], last_pub_year_qua[1], 
              last_pub_year_exp[1], P_count[2], weighted_lin[2], 
              weighted_qua[2], weighted_exp[2], CR_count[2], 
              first_co_ratio1, first_co_ratio2, first_co_ratio12, 
              second_co_ratio1, second_co_ratio2, second_co_ratio12, 
              third_co_ratio1, third_co_ratio2, third_co_ratio12, 
              forth_co_ratio1, forth_co_ratio2, forth_co_ratio12
              fifth_co_ratio1, fifth_co_ratio2, fifth_co_ratio12, 
              sixth_co_ratio1, sixth_co_ratio2, sixth_co_ratio12,
              seventh_co_ratio1, seventh_co_ratio2, seventh_co_ratio12,
              eighth_co_ratio1, eighth_co_ratio2, eighth_co_ratio12,
              CONF_count[0], CONF_count[1], CONF_count[2], 
              last_pub_year_lin[2], last_pub_year_qua[2], last_pub_year_exp[2], 
              num_same_conf, Y[0][0], Y[0][1], 
              Y[0][2], Y[0][3], Y[1][0], 
              Y[1][1], Y[1][2], Y[1][3], 
              Y_binary[0][0], Y_binary[0][1], Y_binary[0][2], 
              Y_binary[0][3], Y_binary[1][0], Y_binary[1][1], 
              Y_binary[1][2], Y_binary[1][3], Y12[0], 
              Y12[1], Y12[2], Y12[3], 
              Y12_binary[0], Y12_binary[1], Y12_binary[2], 
              Y12_binary[3], 
              abs(last_pub_year_lin[0]-last_pub_year_lin[2])**2, 
              abs(last_pub_year_lin[1]-last_pub_year_lin[2])**2, 
              2**abs(last_pub_year_lin[0]-last_pub_year_lin[2]), 
              2**abs(last_pub_year_lin[1]-last_pub_year_lin[2]), 
              )
  return features


# helper

def getAuthorPairs():
  author_pairs = []
  for line in input_file:
    tokens = line.split(' ')
    author_pairs.append((tokens[0], tokens[1]))
  input_file.seek(0)
  return list(OrderedDict.fromkeys(author_pairs))

def getKeysWithValue(dict, v):
  keys = []
  for key, value in dict.iteritems():
    if value == v:
      keys.append(key)
  return keys

# main
def main():

  # generate features of whole dataset
  if len(sys.argv)>5 and sys.argv[5]=='1':

    createHash()

    for ap in co_hash:

      label = get_label(ap[0], ap[1]) if ans_data else '0'

      features = gen_features((ap[0], ap[1]))
      output_file.write(label)
      for i, f in enumerate(features):
        output_file.write(' {0}:{1}'.format(i+1, f))
      output_file.write('\n')
     
  # generate features of whole dataset, which is query data
  elif len(sys.argv)>5 and sys.argv[5]=='-1':

    createHash()

    for line in input_file:
      tokens = line.split(' ')
      author1 = tokens[0]
      author2 = tokens[1][0:-2]
      if int(author1)>int(author2): author1, author2 = author2, author1

      ap = (author1, author2)

      label = get_label(ap[0], ap[1]) if ans_data else '-1'

      features = gen_features((ap[0], ap[1]))
      output_file.write(label)
      for i, f in enumerate(features):
        output_file.write(' {0}:{1}'.format(i+1, f))
      output_file.write('\n')
     
  # input file is a part of past data
  else:

    createHash()

    author_pairs = getAuthorPairs()
    for ap in author_pairs:

      label = get_label(ap[0], ap[1]) if ans_data else '-1'

      features = gen_features((ap[0], ap[1]))

      output_file.write(label)
      for i, f in enumerate(features):
        output_file.write(' {0}:{1}'.format(i+1, f))
      output_file.write('\n')

main()

