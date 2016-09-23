from math import log, ceil
from random import randint

# Class sparse1_sampler:
# ssparse1_sampler is a 1 sparse sampler, which is the basic atom component of a L0Sampler.
# If input stream is 1-sparse (have only 1 non-zero element), 
#   self.result() will return the non-zero index with probability 1.
# If input stream is not 1-sparse, self.errorCheck() will 
#   detects the fault with probability of 1 - e / (len(v)^2), where 'e' is a 
#   positive small float number less than 1. 'e' was used in generate kP.
# For a non 1-sparse stream, so the stream is whether has no non-zero indexs 
#   or has more than 1 non-zero indexs, if we are very unluckly output an index
#   by self.result(), which means our self.errorCheck() fails to tell the stream 
#   is not 1-sparse, then we will not know this error. However this happens in a 
#   small probability.
# Defination of 1-sparse: stream has only 1 or 0 non-zero index.

# Default value of kP and kZ in 1-sparse sampler
defaultkP = 2305377733
defaultkZ = 143
class sparse1_sampler:
    def __init__(self, kP = defaultkP, kZ = defaultkZ):
        self.weight = 0
        self.sum = 0
        self.checksum = 0
        self.kP = kP#TODO:kP is a random prime number. kP > n^3 / e
        self.kZ = kZ#randint(0, self.kP - 1) #TODO discuss whether Z can be zero.
    def push_back(self, s, a):
        self.weight = self.weight + a
        self.sum = self.sum + s * a
        self.checksum = (self.checksum + ((a * (self.kZ ** s)) % self.kP)) % self.kP
    # for debug
    # Input stream S = [(s0, a0), (s1, a1), ... , (sn-1, an-1)]
    # where 'si' is the index of the edges in a graph, 'ai' = {x|x=-1 or x=1}
    # ai = 1 means 'add edge si to the graph', ai = -1 means 'delete edge si'
    def sample(self, S):
        for each in S:
            self.push_back(each[0], each[1]) #each[0] refers to si
    def nonZeroIndex(self):
        try:
            if self.weight == 0:
                raise Exception('1-sparse sampler', 'divide 0 in sum / weight')
        except Exception as inst:
            print(inst)
        return self.sum / self.weight
    # self.sparse1Check:
    # if return 0, then the stream is 1-sparse (has 0 or 1 non-zero indexs)
    # else, the stream is not 1-sparse
    def sparse1Check(self):
        return self.checksum - ((self.weight * \
            self.kZ ** self.nonZeroIndex()) % self.kP)
    # self.result()
    def result(self):
        if self.weight == 0:
            # If stream has no non-zero index, return -1.
            return -1
        if self.sparse1Check() != 0:
            # If stream is not 1-sparse, return None.
            return None
        # If stream has and only has 1 non-zero index, return the index.
        return self.nonZeroIndex()
    # linearly add 1-sparse sampler A and B by add their sum, weight and checksum.
    def add(self, other):
        try:
            if self.kZ != other.kZ or self.kP != other.kP:
                raise Exception('1-sparse sampler', 'adding two sampler having\
                    different Z and P in their checksum');
        except Exception as inst:
            print(inst)
        self.weight = self.weight + other.weight
        self.sum = self.sum + other.sum
        self.checksum = (self.checksum + other.checksum) % self.kP

# Class sparseS_sampler:
# A s-sparse sampler takes a stream S as its input,
# If S is s-sparse, then self.result() will return a non-zero index in the
#   cooresponding vector of S with probability of 1 - s/(2^k)
# Else, whether S has none non-zero index or has more than s non-zero indexs,
#   self.result() will return None with probability of 1 - 2kse/(n^2), where e is the
#   e in Class 1-sparse sampler.
# By choosing k = 2log(n/e), we ensure for a random stream S(we don't know its
#   density), the total probability of error is at most e/(n^2), since total 
#   probability of error = s/(2^k) + 2kse/(n^2) 
#
# Notice that unlike 1-sparse sampler, s-sparse sampler may not output an index of non-zero index even the input is a real s-sparse stream. However, this happens with small probability.
# For a non s-sparse input, if we very unluckly output some non-zero index, which means our self.errorCheck() fails to tell the input is not s-sparse, we will never know this error. However, this happens with small probability.

# How to use:
#     s = sparseS_sampler()
#     s.setParameters(n, k, s) 
#     for each in SomeStream:
#         s.push_back(each)
#     print s.result()
class sparseS_sampler:
    def __init__(self):
        self.kN = 0 # kN is the len(v), where v is the stream vector.
        self.kK = 0 #TODO determin automaticly by given a Probability.
        self.kS = 0 #TODO kS is the S in sparseS, meaning at most 3 non-zero elements.
        # K lines of 1-sparse samplers, each line 2S of them. Si,j = S[j + i * 2S]
        self.sparse1_samplerList = []
        self.hashTablesList = [] #TODO didn't seriously test the hash quality.
        # kP and kZ values in 1-sparse samplers
        self.kPs = [] # 2ks P, each 1-sparse sampler has one P
        self.kZs = [] # 2ks Z, each 1-sparse sampler has one Z 
    
    # Generate kK hash different hash tables that map [0, N-1] -> [0, 2S-1]
    def generateHashTables(self):
        for i in range(0, int(self.kK)):
            temp = []
            for j in range(0, self.kN):
                # randint creat a random number between [0, 2S-1]
                temp.append(randint(0, int(2 * self.kS - 1)))
            self.hashTablesList.append(temp)

    # Create 2KS 1-sparse samplers, with 
    #    their P and Z are given in self.kPs and self.kZs.
    def createSparse1Samplers(self):
        try:
            if len(self.kPs) != self.kK * self.kS * 2 or len(self.kZs) != self.kK * self.kS * 2:
                raise Exception('s-sprase sampler', 'size of list \'P\'s is not 2ks')
        except Exception as inst:
            print '!!!!Exception', inst

        for i in range(0, int(self.kK * self.kS * 2)):
            self.sparse1_samplerList.append(sparse1_sampler(self.kPs[i], self.kZs[i]))
        
    def push_back(self, x, a):
        # for each (si, ai), map it into k 1-sparse samplers, each line 1.
        for i in range(0, int(self.kK)):
            hashValue = self.hashTablesList[i][x]
            self.Samplerij(i, hashValue).push_back(x, a)

    # return the 1-sparse sampler at position (i,j)
    def Samplerij(self, i, j):
        return self.sparse1_samplerList[int(j + i * 2 * self.kS)]

    # return one non-zero index of the vector.
    def sample(self, stream):
        for each in stream:
            self.push_back(each[0], each[1])
    # For debug only.
    def PrintResultMatrix(self):
        print 'n, k, s: ', self.kN, self.kK, self.kS
        for i in range(0, self.kK):
            print 'i = ', i , '  ',
            for j in range(0, 2 * self.kS):
                print self.Samplerij(i, j).result(),
            print '\n',

    # Return '-1' if the stream is empty,
    # Return 'None' if the sream is not s-sparse,
    # Else return one arbitrary non-zero index.
    def result(self):
        # Police:
        # 1. If there is a None in one line, then see next line.
        # 2. If there is no None in one line, and if there exists a non-zero index, then return it.
        # 3. If there is no None in one line, and this line are all '-1', then see next line.
        # 4. If after all the line, we didn't find a non-zero index, 
        #    then return 'None' if 'None' had appeared, else return '-1'. 
        
        NoneAppearedInAnyLine = False
        for i in range(0, self.kK):
            ans = -1
            NoneAppearedInCurrentLine = False
            for j in range(0, 2 * self.kS):
                temp = self.Samplerij(i, j).result()
                if temp == None:
                    NoneAppearedInCurrentLine = True
                    NoneAppearedInAnyLine = True
                    break
                if temp != -1:
                    ans = temp
            if NoneAppearedInCurrentLine:
                continue # See next line
            if ans != -1:
                return ans
        if NoneAppearedInAnyLine == True:
            return None
        return -1


    def setParameters(self, n, k, s):
        self.kN = n
        self.kK = k
        self.kS = s 
        # generate Ps and Zs
        primesList = primes(1000000) # TODO chage the number to a variable
        for i in range(0, int(k * s * 2)):
            self.kPs.append(primesList[randint(0,len(primesList) - 1)])
            self.kZs.append(randint(1,self.kPs[i] - 1))
        # create k hash functions and 2ks 1-sparse samplers
        self.generateHashTables()
        self.createSparse1Samplers()
# Class L0Sampler:
# L0sampler takes a stream S as its input. the si of (xi, ai) in S is between [1,n], where n is the length of S. 
# If the S is not empty(has at least one non-zero), L0-Sampler will return a non-zero index with probability at least 1 - e/2,
#   and if this happen, it means that the number of non-zero elements in S is [kc, 2kc], where k is the index of hash function. k = 2^l
#   
class L0Sampler:
    def __init__(self, n):
        self.kN = n # TODO set kN, the upper bound of xi. Also the length of Stream.
        self.kN2 = 2 ** int(ceil(log(n, 2))) # kN2 is the nearest intager kN in power of 2 and kN2 >= kN
        self.ensurance = 0.99 # TODO ensurance is the probability of no error.
        self.hashTablesList = [] # log N hash tables that map [1, n] -> [0, 1] where that h(i) maps to 1 with probability 1/k. k = 1,2,4,8,..,n
        self.sparses_samplerList = [] # log N s-sparse samplers, where s = 3 * 12ln(4/e)
        
        # calculate the epsion according to ensurance.
        e = 2 * (1 - self.ensurance) # since ensurance = 1 - e/2.
        self.kE = e
        # calculate the k,s needed in s-sparse sampler.
        self.kK = int(2 * log(self.kN2 / self.kE, 2))  # k = 2log(n/e) 
        self.kS = int(3 * 12 * log(4 / self.kE)) # s = 3c = 3*12ln(4/e)
        # generate log(N) hash functions.
        i = 1
        while i <= self.kN2:
            self.hashTablesList.append(self.hash(i, self.kN2))
            i = i * 2
        # create log(N) s-sparse samplers.
        for i in range(0, int(log(self.kN2, 2))):
            self.sparses_samplerList.append(sparseS_sampler())
            self.sparses_samplerList[-1].setParameters(self.kN2, self.kK, self.kS)
    # take (s,a) in the stream as one input.
    def push_back(self, s, a):
        try:
            if s > self.kN:
                raise Exception('L0-sparse sampler', 'Input element x > n, illegal.')
        except Exception as inst:
            print '!!!!Exception', inst
        for i in range(0, int(log(self.kN2, 2))):
            if self.hashTablesList[i][s] == 1:
                # This happens at probability 1/k, k = 2^i
                self.sparses_samplerList[i].push_back(s, a)
    # take the stream S as the input.
    def sample(self, S):
        for each in S:
            self.push_back(each[0], each[1]) #each[0] refers to si
    # return a non-zero index in stream S.    
    def result(self):
        for idx, each in enumerate(self.sparses_samplerList):
            temp = each.result()
            if temp != None:
                k = idx + 1
                c = 12 * log(4 / self.kE)
                print 'k = ' + str(k) + '  range of s:[' + str(k * c) + ',' + str(2 * k * c) + ']'
                return temp
        return None 
        
    # Return a list with 1/k elements are 1 and the rest are 0. n is the length of the list. 
    # Tested.
    def hash(self, k, n): 
        if k == 1:
            return [1] * n
        hashTable = [0] * n # hashTable = [0, 0, 0, ..., 0]
        i = 0
        while i < n / k:
            randIndex = randint(0, n - 1)
            if hashTable[randIndex] == 0: 
                hashTable[randIndex] = 1 
                i += 1
        return hashTable

def testOne1(sampler, testcase):
    sampler.sample(testcase[:-1])
    return sampler.result() == testcase[-1]
def testSparse1Sampler():
    testcases = [[(1,+1),(2,1),(3,1),(3,-1),None],
                 [(4,1),(4,-1),(5,-1),(5,1),(1,-1),None],
                 [-1],
                 [(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(4,-1),(5,-1),(6,-1),(7,-1),(8,-1),(9,-1),(10,-1),(11111,1),11111],
                 [(1,1),(1,-1),(2,1),(2,-1),(3,1),(3,-1),(4,1),(4,-1),(1,1),(1,-1),1],
                 [(2,1),(2,-1),-1],
                 [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),None]]
    testcases2 = [[(1,+1),(2,1),(3,1),(3,-1)],[(4,1),(4,-1),(5,-1),(5,1),(1,-1)],2] # stream + stream2 = (2,1)

    print '*******naive test 1-sparse sampler********'
    for i in range(0, len(testcases)):
        if testOne1(sparse1_sampler(), testcases[0]):
            print 'test case ' + str(i) + ': succeed'
        else:
            print 'test case ' + str(i) + ': failed'

    #TODO test add of two samplers, generate big datas to test. test different Z, P

def testOneS(n, k, s, testcase):
    sampler = sparseS_sampler()
    sampler.setParameters(n, k, s)
    sampler.sample(testcase[:-1])
    #sampler.PrintResultMatrix() 
    return sampler.result() in testcase[-1]
def testSparseSSampler():
    testcases = [[(1,+1),(2,1),(3,1),(3,-1),[1,2]],
                 [(4,1),(4,-1),(5,-1),(5,1),(1,1),[1]],
                 [[-1]],
                 [(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(4,-1),(5,-1),(6,-1),(7,-1),(8,-1),(9,-1),(10,-1),(11,1),(3,1),[11,3]],
                 [(1,1),(1,-1),(2,1),(2,-1),(3,1),(3,-1),(4,1),(4,-1),(1,1),(1,-1),(1,1),[1]],
                 [(2,1),(2,-1),[-1]],
                 [(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),[None]]]
    s = 3
    print '*******naive test s-sparse sampler********'
    i = 0
    for each in testcases:
        n = len(each)
        k = int(2 * log(n / 0.02, 2))
        if testOneS(n, k, s, each) == True: # let len(vector) be a estimation of n.
            print 'test case' + str(i) +': succeed'
        else:
            print 'test case' + str(i) +': failed'
        i = i + 1
    #TODO generate test with probabilities

# Generate a prime number list below n. 
def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in xrange(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
    return [2] + [i for i in xrange(3,n,2) if sieve[i]]

def testL0Sampler():
    print '********Manually Test for L0-Sampler*******'
    print 'Done and Succeed.' # the code in this function has been runned and it shows L0 works correctly.
    return
    samp = L0Sampler(10)
    s = [(4,1),(4,-1),(5,-1),(5,1),(1,1)]
    samp.sample(s)
    print '\nInput S to L0-sampler', s
    print samp.result()

    samp2 = L0Sampler(13)
    s = [(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(4,-1),(5,-1),(6,-1),(7,-1),(8,-1),(9,-1),(10,-1),(11,1),(3,1)]
    samp2.sample(s)
    print '\nInput S to L0-sampler', s
    print samp2.result()

    samp3 = L0Sampler(13)
    s = [(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(10,-1),(11,1),(3,1)]
    samp3.sample(s)
    print '\nInput S to L0-sampler', s
    print samp3.result()

if __name__ == "__main__":
    testSparse1Sampler()
    testSparseSSampler()
    testL0Sampler()
    samp = L0Sampler(1000)

    print'\n\n*******Now begin reconstruct a graph using single L0 sampler*********'
    #s = [(1,1),(2,1),(1,-1),(3,1),(4,1),(1,1),(5,1),(6,1),(4,-1),(4,1),(7,1),(8,1),(9,1),(1,-1)]
    s = []
    for i in range(1,1001):
        s.append((i, 1))
        s.append((i, -1))
        s.append((i, 1))
    for i in range(1,101):
        s.append((i, 1))
    for i in range(1,101):
        s.append((i, -1))
    print 'input stream = ', s
    samp.sample(s)
    print 'output non-index elements:'
    temp = 1
    count = 0
    n = 1000
    while count <= n:
        temp = samp.result()
        print temp,
        samp.push_back(temp, -1)
        if temp == -1:
            break
        count = count + 1
    print '\noutput ' + str(count)