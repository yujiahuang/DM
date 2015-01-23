# DM
##Data Mining Final Project


P1: total number of papers of author1

P2: total number of papers of author2

P12: total number of papers in collaboration of author1. and author2

CR1: total number of collaborators of author1

CR2: total number of collaborators of author2

CN1: total number of collaborations of author1

CN2: total number of collaborations of author2

CN12: total number of collaborations of author1. and author2 (=P12)

W1: weighted publication sum of papers of author1. ((2008->1, 2009->2, ..., 2012->5))

W2: weighted publication sum of papers of author2 ((2008->1, 2009->2, ..., 2012->5))

W12: weighted collaboration sum of author1. and author2 (2008->1, 2009->2, ..., 2012->5)

// id
not included

// auto-features

1. P1
1. P2
1. CR1
1. CR2
1. CN1
1. CN2
1. W1
1. W2
1. last collaboration time of author1. with anyone
1. last collaboration time of author2 with anyone

// co-features

1. P12
1. W12
1. first collaboration ratio of author1. (P12/P1)
1. first collaboration ratio of author2 (P12/P2)
1. first collaboration ratio of author1. + author2 (P12/(P1+P2))
1. second collaboration ratio of author1. (CN12/CN1)
1. second collaboration ratio of author2 (CN12/CN2)
1. second collaboration ratio of author1. + author2 (CN12/(CN1+CN2))
1. third collaboration ratio of author1. (1/CR1)
1. third collaboration ratio of author2 (1/CR2)
1. forth collaboration ratio of author1. (W12/W1)
1. forth collaboration ratio of author2 (W12/W2)
1. last collaboration time of author1. and author2
1. how many times author1. and author2 publish in the same conference (MAX_i(author1. and author2 in conf_i))


// all time features has the following formats
o. linear: 1, 2, 3, ...
o. quadratic: 1, 4, 9, ...
o. exponential: 2, 4, 8, ...


