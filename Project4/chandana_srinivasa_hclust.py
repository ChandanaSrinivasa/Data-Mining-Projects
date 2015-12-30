import sys
import itertools
import heapq
import math



def find_centroid(cluster, data_points_list):
    centroid_list = list()
    cluster_centroid_list = list()
    cluster_length = len(cluster)

    for i in range(0,dimension):
        centroid_list.append(0.0)
    for i in range(0,cluster_length):
        cluster_centroid_list.append(data_points_list[cluster[i]])
    for i in range(0,dimension):
        for j in range(0,cluster_length):
            centroid_list[i] += cluster_centroid_list[j][i]
        centroid_list[i] = centroid_list[i]/cluster_length
    return centroid_list


def find_euclidean_dist(clusterA,clusterB,data_points_list):
    sumOfSquares = 0

    if len(clusterA) == 1:
        centroidA = data_points_list[clusterA[0]]
    else:
        centroidA = find_centroid(clusterA,data_points_list)

    if len(clusterB) == 1:
        centroidB = data_points_list[clusterB[0]]
    else:
        centroidB = find_centroid(clusterB,data_points_list)

    for i in range(0,dimension):
        x = centroidA[i]
        y = centroidB[i]
        sumOfSquares += pow((x-y),2)
    euclidean_dist = math.sqrt(sumOfSquares)
    return euclidean_dist


def find_cluster_points_dist(i,points_index,data_points_list,heap):
	clusterA = list(points_index[i])
	j = i+1
	for k in range(j,len(points_index)):
		clusterB = list(points_index[k])
		euc_dist = find_euclidean_dist(clusterA,clusterB,data_points_list)
		euc_dist_lst = [euc_dist,[clusterA,clusterB]]
		heapq.heappush(heap,euc_dist_lst)
	return heap	


def find_cluster(heap,n):
    clusters_dict = dict()
    while n > 1:
        closest_cluster = heapq.heappop(heap)
        cluster_a = closest_cluster[1][0]
        cluster_b = closest_cluster[1][1]
        if cluster_a in points_index and cluster_b in points_index:
            points_index.remove(cluster_a)
            points_index.remove(cluster_b)
            merged_cluster = sorted(list(set(cluster_a) | set(cluster_b)))
            points_index.insert(0,merged_cluster)
            heap = find_cluster_points_dist(0,points_index,data_points_list,heap)
            n -= 1
            clusters_dict[n] = list(points_index)
    return clusters_dict

def generate_heap(n):
    heap = list()
    for i in range(0,n-1):
        heap = find_cluster_points_dist(i,points_index,data_points_list,heap)
    return heap

def generate_cluster_pairs(pairs,cluster):
    new_pairs = list(itertools.combinations(cluster,2))
    pairs += new_pairs
    return pairs

def find_gold_standard(lines):
    gold_std_dict = dict()
    index = 0
    for eachItem in lines:
        point = eachItem.strip().split(',')
        cluster_name = point[-1]
        gold_std_dict.setdefault(cluster_name,[])
        gold_points_list=gold_std_dict[cluster_name]
        gold_points_list.append(index)
        gold_std_dict[cluster_name] = gold_points_list
        index += 1
    return gold_std_dict

def find_accuracy(k_clusters,lines):
    alg_pairs = list()
    gold_pairs = list()
    for cluster in k_clusters:
        alg_pairs = generate_cluster_pairs(alg_pairs,cluster)

    gold_std_dict = find_gold_standard(lines)

    for key,value in gold_std_dict.items():
        gold_pairs = generate_cluster_pairs(gold_pairs,value)

    commonPairsInAlgAndGoldStd = set(alg_pairs).intersection(gold_pairs)
    total_pairs_from_alg = float(len(alg_pairs))
    total_pairs_in_gold_std = float(len(gold_pairs))
    total_common_pairs = float(len(commonPairsInAlgAndGoldStd))

    precision = total_common_pairs/total_pairs_from_alg

    recall = total_common_pairs/total_pairs_in_gold_std

    return precision,recall

def print_cluster(k_clusters):
    for i in range(0,len(k_clusters)):
        print(k_clusters[i])

ip_file = open(sys.argv[1],'rb')
k = int(sys.argv[2])
lines = ip_file.readlines()
data_points_list = list()
points_index = list()
n = 0
dimension = 0
for eachLine in lines:
    point=eachLine.strip().split(',')
    del point[-1]  #deleting last element of the list
    point=[float(i) for i in point]
    data_points_list.append(point)
    points_index.append([n])
    n += 1

dimension = len(data_points_list[0])
heap = generate_heap(n)
clusters_dict = find_cluster(heap,n)
precision,recall = find_accuracy(clusters_dict[k],lines)
print(precision)
print(recall)
print_cluster(clusters_dict[k])
