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

// co-features

1: first collaboration ratio of author1 and author2 ( ( max(P12/P1, P12/P2) or P12/(P1+P2) ) OR split into three features: P12/P1, P12/P2, P12/(P1+P2))
2: second collaboration ratio of author1 and author2 ( ( max(CN12/CN1, CN12/CN2) or CN12/(CN1+CN2) ) OR split into three features: CN12/CN1, CN12/CN2, CN12/(CN1+CN2))
3: third collaboration ratio of author1 and author2 ( (CN12 != 0) ? max(1/CR1, 1/CR2) : 0 ) OR split into two features: (CN12 != 0) ? 1/CR1 : 0, (CN12 != 0) ? 1/CR2 : 0 )
4: last collaboration time of author1 and author2
5: how many times author1 and author2 publish in the same conference (conference can generate more features if necessary)
6: degrees of separation of author1 and author2

// auto-features

7: total number of collaborators of author1 (CR1)
8: total number of collaborators of author2 (CR2)
9: total number of collaborations of author1 (CN1)
10: total number of collaborations of author2 (CN2)
11: last collaboration time of author1 with anyone
12: last collaboration time of author2 with anyone
13: total number of papers of author1 (P1)
14: total number of papers of author2 (P2)
15: last publication time of author1
16: last publicaiton time of author2


// time features can use real number to represent, such as 2013->1000 2012->500 2011->200 2010->100
```
