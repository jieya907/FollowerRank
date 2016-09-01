from scipy import linalg as LA
import pprint
import numpy
import pickle
from collections import defaultdict
#network = pickle.load( open( "topusers0_3000.p", "rb" ) )

def id_2_index(network) :
    lookup = {}
    numfollowing = defaultdict(int)
    i = 0
    for user, followers in network.items():
        if user not in lookup:
            lookup[user] = i
            i += 1
        for follower in followers: 
            numfollowing[follower] += 1
            if follower not in lookup:
                lookup[follower] = i
                i += 1
    return lookup, numfollowing

def to_sparse_matrix(network, user_id, numfollowing):
    matrix = []
    for user, followers in network.items():
        for follower in followers:
            matrix.append(((user_id[user],
                user_id[follower]), numfollowing[follower]))
    return matrix, len(user_id)

def to_numpy (sparse, numUser) :
    a = numpy.zeros(shape=(numUser,numUser))
    for entry in sparse:
        (i, j), n = entry
        a[i, j] = 1.0/n
    return numpy.asmatrix(a)

testinput = {u'1': [u'3', u'4'],
             u'2': [u'1'],
             u'3': [u'1', u'2', u'4'],
             u'4': [u'1', u'2']}

index, following = id_2_index(testinput)
sparse,n = to_sparse_matrix(testinput,index, following)

m = to_numpy(sparse, n)

pprint.pprint(index)
pprint.pprint(following)
print m
evals, e_vecs = LA.eig(m)
print evals
print e_vecs[evals.index(1)]

