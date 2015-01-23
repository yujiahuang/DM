# DM
Data Mining Final Project

```
P1: total number of papers of author1
P2: total number of papers of author2
P12: total number of papers in collaboration of author1 and author2
CR1: total number of collaborators of author1
CR2: total number of collaborators of author2
CN1: total number of collaborations of author1
CN2: total number of collaborations of author2
CN12: total number of collaborations of author1 and author2 (=P12)

// id

<!-- 1. author1 id
1. author2 id -->

// auto-features

1. total number of papers of author1 (P1)
1. total number of papers of author2 (P2)
1. total number of collaborators of author1 (CR1)
1. total number of collaborators of author2 (CR2)
1. total number of collaborations of author1 (CN1)
1. total number of collaborations of author2 (CN2)
1. last collaboration time of author1 with anyone
1. last collaboration time of author2 with anyone

// co-features

1. collaboration times of author1 and author2
1. weighted collaboration times of author1 and author2 (2008->1, 2009->2, ..., 2012->5)
1. first collaboration ratio of author1 (P12/P1)
1. first collaboration ratio of author2 (P12/P2)
1. first collaboration ratio of author1 + author2 (P12/(P1+P2))
1. second collaboration ratio of author1 (CN12/CN1)
1. second collaboration ratio of author2 (CN12/CN2)
1. second collaboration ratio of author1 + author2 (CN12/(CN1+CN2))
1. third collaboration ratio of author1 1/CR1
1. third collaboration ratio of author2 1/CR2
1. last collaboration time of author1 and author2
1. how many times author1 and author2 publish in the same conference (MAX_i(author1 and author2 in conf_i))
1. heterogeneous degrees of separation of author1 and anthor2 (both authors and conferences are nodes, if disconnected set to 9999999)
1. homogeneous degrees of separation of author1 and author2 (only author links considered, if disconneted set to 9999999)


// time features
o. linear: 1, 2, 3, ...
o. quadratic: 1, 4, 9, ...
o. exponential: 2, 4, 8, ...

```
