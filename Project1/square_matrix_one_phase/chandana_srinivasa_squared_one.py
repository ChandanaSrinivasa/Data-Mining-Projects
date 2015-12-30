import MapReduce
import sys


mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    l=m=n=5
    for k in range(0,n):
      mr.emit_intermediate((record[0],k),['A',record[1],record[2]])

    for i in range(0,l):
      mr.emit_intermediate((i,record[1]),['A',record[0],record[2]])

def reducer(key, list_of_values):
    # key: (i,k)
    # value: Sumj(A[i,j] * B[j,k])
    length = len(list_of_values)
    sum = 0
    for x in range(0,length-1):
      for y in range(x+1,length):
          if list_of_values[x][1] == list_of_values[y][1]:
            prod = list_of_values[x][2]*list_of_values[y][2]
            sum += prod
    mr.emit([key[0],key[1],sum])
  
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)