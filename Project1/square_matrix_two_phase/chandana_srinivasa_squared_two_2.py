import MapReduce
import sys

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key:  (i,k)
    # value: (A[ij] * B[jk])
    mr.emit_intermediate((record[0],record[1]),record[2])



def reducer(key, list_of_values):
    #emit [i,k,Sum(values)]
    product_list = list_of_values
    items = len(product_list)
    sum = 0
    for i in range(0,items):
      sum += product_list[i]
    mr.emit([key[0],key[1],sum])


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
