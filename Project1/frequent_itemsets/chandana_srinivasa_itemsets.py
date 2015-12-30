import MapReduce
import sys
import re
import itertools


mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    value = record
    itemsets = itertools.combinations(value,2)
    for each_pair in itemsets:
      mr.emit_intermediate(each_pair,1)

def reducer(key, list_of_values):
    # key: 2-itemsets
    total = 0
    for value in list_of_values:
      total += value
    if total >= 100:
      mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
