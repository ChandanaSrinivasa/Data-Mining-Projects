import MapReduce
import sys
import re
from collections import Counter


mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[0]
    value = record[1]
    words = re.findall(r'\w+',value.lower())
    for w in words:
      mr.emit_intermediate(w,key)

def reducer(key, list_of_values):
    cnt = Counter()
    for v in list_of_values:
      cnt[v] += 1
    df = len(cnt)
    tf_list=[]
    for each_file_name in cnt:
      tf_key_value = []
      tf_key_value.append(each_file_name)
      tf_key_value.append(cnt[each_file_name])
      tf_list.append(tf_key_value)
    mr.emit([key,df,tf_list])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
