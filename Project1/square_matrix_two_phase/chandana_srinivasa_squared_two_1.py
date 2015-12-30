import MapReduce
import sys


mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    mr.emit_intermediate(record[1],['A',record[0],record[2]])
    mr.emit_intermediate(record[0],['B',record[1],record[2]])

def reducer(key, list_of_values):
    length = len(list_of_values)
    for i in range(0,length):
      if list_of_values[i][0]=='A':
        for j in range(0,length):
          if list_of_values[j][0]=='B':
            mr.emit([list_of_values[i][1],list_of_values[j][1],list_of_values[i][2]*list_of_values[j][2]])

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
