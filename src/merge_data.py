# python merge_data.py (1) output_path (2) -b (3) basis_data (4) -a (5) append_data

import sys

basis_data = None
append_data = None
output = open(sys.argv[1], 'w+')

if sys.argv[2] == '-b':
  basis_data = open(sys.argv[3], 'r')

# copy lines in basis_data
for line in basis_data:
  output.write(line)
basis_data.seek(0)

# copy non-repeated data in append_data
if sys.argv[4] == '-a' and len(sys.argv)>5:
  append_data_paths = sys.argv[5].split(' ')
  for p in append_data_paths:
    append_data = open(p, 'r')
    for line in append_data:
      repeated = False
      for written_line in basis_data:
        if line == written_line:
          repeated = True
          break
      if not repeated: output.write(line)
      basis_data.seek(0)
    append_data.close()