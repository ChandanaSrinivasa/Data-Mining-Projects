from sys import argv
from math import sqrt

def pearson_correlation(user1, user2):
    sum1 = 0
    sum2 = 0
    total1 = 0
    total2 = 0
    avg1 = 0
    avg2 = 0
    co_sum1 = 0
    co_sum2 = 0
    moviesRatingDictOfUser1 = {}
    moviesRatingDictOfUser2 = {}
    for keys in pearsonDict:
        if keys[0] == user1:
            moviesRatingDictOfUser1[keys[1]] = float(pearsonDict.get(keys))
            sum1 += float(pearsonDict.get(keys))
            total1 += 1
        elif keys[0] == user2:
            moviesRatingDictOfUser2[keys[1]] = float(pearsonDict.get(keys))
            sum2 += float(pearsonDict.get(keys))
            total2 += 1
    avg1 = sum1 / total1
    avg2 = sum2 / total2
    #print "Average of User 1 is:"
    #print avg1
    #print "Average of User 2 is:"
    #print avg2
    #print moviesRatingDictOfUser1
    #print moviesRatingDictOfUser2
    commonMovies = set(moviesRatingDictOfUser1.keys()).intersection(moviesRatingDictOfUser2.keys())
    #print(commonMovies)
    numerator = 0
    u1_square_summation = 0
    u2_square_summation = 0
    for movie in commonMovies:
        ratingMovieU1 = moviesRatingDictOfUser1.get(movie)
        ratingMovieU2 = moviesRatingDictOfUser2.get(movie)
        rUI_rU = float(ratingMovieU1) - avg1
        rVI_rV = float(ratingMovieU2) - avg2
        productNumerator = rUI_rU * rVI_rV
        numerator += productNumerator
        rUI_rU_square = float(rUI_rU * rUI_rU)
        rVI_rV_square = float(rVI_rV * rVI_rV)
        u1_square_summation += rUI_rU_square
        u2_square_summation += rVI_rV_square
    u1_square_summation_sqrt = sqrt(u1_square_summation)
    u2_square_summation_sqrt = sqrt(u2_square_summation)
    denominator = u1_square_summation_sqrt * u2_square_summation_sqrt
    if denominator == 0 or numerator == 0:
        pearsonCorrelation = 0
    else:
        pearsonCorrelation = numerator / denominator
    #print(pearsonCorrelation)
    return pearsonCorrelation

def K_nearest_neighbors(user1, k):
    userSet = set()
    pearsonSimDict = {}
    k_nearest_neighbour_sim_dict = {}
    for keys in pearsonDict:
        if keys[0] != user1:
            userSet.add(keys[0])
    #print userSet
    for eachUser in userSet:
        pc = pearson_correlation(user1,eachUser)
        pearsonSimDict[eachUser] = float(pc)
    sortedPSimList =  sorted(pearsonSimDict.items(), key=lambda x: (-x[1], x[0]))
    #print(sortedPSimList)
    for i in range(int(k)):
        #print str(sortedPSimList[i][0]) + " " + str(sortedPSimList[i][1])
        print(str(sortedPSimList[i][0]) + " " + str(sortedPSimList[i][1]))
        k_nearest_neighbour_sim_dict[sortedPSimList[i][0]] = sortedPSimList[i][1]
    return k_nearest_neighbour_sim_dict

def Predict(user1, item, k_nearest_neighbors):
    #print pearsonDict
    #print k_nearest_neighbors
    numerator = 0
    denominator = 0
    itemRatingList = []
    similarityList = []
    #print item
    for each_k_nn in k_nearest_neighbors:
        #print "-----"+each_k_nn+"--------"
        for keys in pearsonDict:
            if keys[0] == each_k_nn and keys[1] == item:
                #print "~~~~~"+each_k_nn+"~~~~~"
                itemRatingList.append(float(pearsonDict.get(keys)))
                similarityList.append(float(k_nearest_neighbors.get(each_k_nn)))
                denominator += float(k_nearest_neighbors.get(each_k_nn))

    for i in range(0, len(itemRatingList)):
        prod = itemRatingList[i] * similarityList[i]
        numerator += prod

    if numerator == 0 or denominator == 0:
        prediction = 0
    else:
        prediction = numerator / denominator

    #print itemRatingList
    #print similarityList
    #print prediction
    print('\n')
    print(prediction)



user_ID = argv[2]
movie_ID = argv[3]
k = argv[4]
#print user_ID
#print movie_ID
#print k
ratingFile = open(argv[1], "rb")

pearsonDict = {}


for eachLine in ratingFile:
    line = eachLine.strip().split('\t')
    userMovieTuple = ()
    userId = (line[0],)
    rating = line[1]
    movieTitle = line[2]
    userMovieTuple = userId + (movieTitle,)
    pearsonDict[userMovieTuple] = rating

#print "Utility Matrix in the form of Dictionary:"
#print pearsonDict

#pearson_correlation('6632e5b3-89cc-461c-aaf7-06e69e634333','edc4c49c-d263-4d37-bc57-da5f7a344800')

k_nearest_neighbors_dict = K_nearest_neighbors(user_ID, k)

Predict(user_ID, movie_ID, k_nearest_neighbors_dict)