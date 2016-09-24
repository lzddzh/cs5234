# This script is a implementation of the 2 algorithms descriped in Problem Set 4(as well in Pset1).
# And we used some random input data to test which one is better.
# By Tony Liu, Sep 24.
from random import randint
import numpy as np

class counter_sampler:
    def __init__(self, A, B, primeNum):
        self.A = A # the number of rows of the counters.
        self.B = B # the number of collums of the counters.
        self.Prime = primeNum
        self.maxNumInStream = 0
        self.counters = np.zeros((A, B), dtype='int64') # assign counters with a A*B matrix with all zero element.
        # we have A different (ka,kb) paris as the parameters of 
        #   hashfunction(value, (ka, kb)), so equvalently we have A different hash functions.
        self.hashParameters = [] 
        for i in range(0, self.A):
            self.hashParameters.append((randint(1, self.Prime - 1), randint(1, self.Prime - 1)))
    # input an item in the stream.
    def push(self, num):
        if self.maxNumInStream < num:
            self.maxNumInStream = num
        for i in range(0, self.A):
            abPair = self.hashParameters[i] # abPair = (ka, kb)
            counterIndex = self.hashfunction(num, abPair)
            self.counters[i][counterIndex] = self.counters[i][counterIndex] + 1
    # input all the items in the stream.
    def input(self, s):
        for each in s:
            self.push(each)
    # a standard uniform hash function: a * x + b.
    # map a number to [0, self.B - 1]
    def hashfunction(self, value, (ka, kb)):
        try:
            if (self.Prime < self.B * 10):
                raise Exception('hashfunction', 'P is not big enough, we must let P >> B')
        except Exception as inst:
            print inst
        return (ka * value + kb) % self.Prime % self.B
    # Algorithm 1 in the Pset4, using the minimum value as estimation.
    def algorithm1count(self, num):
        mini = 2**10000 # First set mini to +inf.
        for i in range(0,self.A):
            counterIndex = self.hashfunction(num, self.hashParameters[i])
            if mini > self.counters[i][counterIndex]:
                mini = self.counters[i][counterIndex] 
        return mini
    # Return all the result of algorithm1
    def result1(self):
        result = []
        for i in range(0, self.maxNumInStream + 1):
            result.append(self.algorithm1count(i))
        return result

    def algorithm2count(self, num):
        estimate = []
        for i in range(0,self.A):
            counterIndex = self.hashfunction(num, self.hashParameters[i])
            if counterIndex % 2 == 0: # even number
                l = self.counters[i][counterIndex]
                r = self.counters[i][counterIndex + 1]
                estimate.append(l - r)
            else:
                l = self.counters[i][counterIndex - 1]
                r = self.counters[i][counterIndex]
                estimate.append(l - r)
        return int(np.median(np.array(estimate)))

    def result2(self):
        result = []
        for i in range(0, self.maxNumInStream + 1):
            result.append(self.algorithm2count(i))
        return result

# Generate a prime number list below n. 
def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in xrange(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
    return [2] + [i for i in xrange(3,n,2) if sieve[i]]

# generate a new stream [s1, s2, s3, ..., sN], where si <= M.
def newStream(M, N):
    stream = []
    for i in range(0, N):
        stream.append(randint(1,M))
    return stream

def correctRate(stream, result):
    count = [0] * (max(stream) + 1)
    for each in stream:
        count[each] = count[each] + 1
    if len(count) != len(result):
        print "result array size is not correct."
        return
    s = 0.0
    for i in range(0, len(count)):
        if count[i] == result[i]:
            s = s + 1
    return s / len(count)

if __name__ == "__main__":
    S = newStream(1000, 100)
    print S
    sam = counter_sampler(7, 100, primes(10000)[-1])
    sam.input(S)
        
    print correctRate(S, sam.result1())
    print correctRate(S, sam.result2())

