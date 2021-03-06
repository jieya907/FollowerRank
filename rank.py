from scipy import linalg as LA
import pprint
import numpy
import pickle
from collections import defaultdict

def id_2_index(network) :
    """
    Scan through the network and return a map between the userID to its
    index in this program. and a map between user id to the number of
    people its following.
    """
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
    """
    Given the network graph, the user_id, and following mappings, return
    a sparse representation of the matrix for page rank.
    """
    matrix = []
    for user, followers in network.items():
        for follower in followers:
            matrix.append(((user_id[user],
                user_id[follower]), numfollowing[follower]))
    return matrix, len(user_id)

def to_numpy (sparse, numUser) :
    """
    Giving a sparse representation of the matrix, i.e. a list of entries,
    return a numpy matrix representation of this matrix.
    """
    a = numpy.zeros(shape=(numUser,numUser))
    for entry in sparse:
        (i, j), n = entry
        a[i, j] = 1.0/n
    return numpy.asmatrix(a)

def eigen(a, t, iterations):
    """
    Calculate the eigenvector whose eigenvalue is 1 by construction a matrix
    for multiplication and multiply it for iterations times.
    By linear algebra, this value should converge.
    """
    #initialize the S matrix
    n = len(a) 
    s = numpy.empty([n, n])
    s.fill(1.0/n)
    s = numpy.asmatrix(s)
    print s
    print a
    #print t
    # Calculating the transformation matrix 
    tmatrix = (1 - t) * a + t * s
    # Initialize the vector
    v = numpy.empty([n, 1])
    v.fill(0)
    v[0][0] = 1
    v = numpy.asmatrix(v)
    print tmatrix
    print v
    #print v.shape
    #print tmatrix.shape
    for i in range(iterations):
        v = tmatrix * v
    return v

testinput = {u'1': [u'3', u'4'],
             u'2': [u'1'],
             u'3': [u'1', u'2', u'4'],
             u'4': [u'1', u'2']}

def output_vec(network):
    """
    Output the final rank calculated by the numpy eigenvector library.
    """
    index, following = id_2_index(network)
    sparse,n = to_sparse_matrix(network,index, following)
    m = to_numpy(sparse, n)
    print m[2988,2331]
    evals, e_vecs = LA.eig(m)
    print evals
    print e_vecs

def count_num_dangling(following) :
    """
    Count the number of dangling users in the graph, i.e. users who do not
    follow any one.
    """
    num_dangling = 0
    for user, num in following.items():
        if num == 0 :
            num_dangling += 1
    return num_dangling;

def output_converge(network, iterations):
    """
    Output the rank calculated by the iterative algorithm.
    """
    index, following = id_2_index(network)
    #print count_num_dangling(following)
    sparse,n = to_sparse_matrix(network,index, following)
    m = to_numpy(sparse, n)
    v = eigen(m, 0.15, iterations)
    return v
network = pickle.load( open( "topusers0_3000.p", "rb" ) )
#output_vec(testinput)
#pprint.pprint(network)
#output_vec(network)
#print output_converge(testinput,50)

vector = output_converge(network, 100) * 1000
print vector
print vector.max()
print numpy.argmax(vector)
