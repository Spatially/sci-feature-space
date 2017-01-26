#
# miff: A module that lets you define a multivariate feature space, and compute a distance
# metric between its elements.
#
# A "feature space" as defined in this module is just a set of individual features, which
# each may be real/integer/categorical/boolean and scalar/vector valued. So for example
# you could have a feature space describing census blocks, where each element of the space
# consists of the name of the town it falls into, its area in square kilometers, the income
# distribution of its inhabitants, and the median age of all residents. There is no limit to the
# Number of features that can be defined for a feature space.
#
# This module then provides a flexible framework for computing scalar distance metrics for the
# elements of this feature space. The general approach is that each individual feature
# is associated with a method for computing a scalar distance metric for that feature individually.
# You can choose between several different per-feature distance metrics (e.g. manhattan distance,
# cosine distance, etc.) or define your own.
#
# This module then provides routines for scaling the per-feature distance metrics to a comparable
# range. For example if a feature space contains both median age and median income (in dollars),
# the individual differences are not really comparable: an age difference of 50 years is
# probably a lot more significant than an income difference of 50 dollars. So this module contains
# a choice of methods that can be used to map per-feature difference values into the range
# [0 1] so that they are more directly comparable.
#
# This module combines the re-mapped metric values using a sinmple weighted sum. The weights
# are user-defined.
#


import numpy as np


#
# Define a few standard difference metrics. Each one of these takes two
# inputs and returns a scalar distance value.
#

def EuclideanDistance(a, b):
    d = np.sqrt(np.sum((a-b)**2))
    return d


def ManhattanDistance(a, b):
    d = np.sum(np.abs(a - b))
    return d    
    
    
def MaxAbsDistance(a, b):
    d = np.maximum(np.abs(a - b))
    return d
    
    
def CosineDistance(a, b):
    d = 1.0 - np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)
    return d
    
    
def DiscreteDistance(a, b):
    d = 1.0
    if a == b:
        d = 0.0
    return d


# This function, which computes the Hellinger distance, first nromalizes the 
# input vectors so that they sum to 1.0.
def HellingerDistance(a, b):
    aa = a / np.sum(a)
    bb = b / np.sum(b)
    bc = 0.0
    for i in range(len(aa)):
        bc = bc + np.sqrt(aa[i] * bb[i])
    d = np.sqrt(1-bc)
    return(d)


#
# Remapping functions. These are functions that map a metric value into the 
# range [0, 1].
#

def LinearRemap(d, r):
    t = np.minimum(d / r, 1.0)
    return t


def ExponentialRemap(d, r):
    t = 1.0 - np.exp(-d / r)
    return t


#
# The "FeatureSpace" class defines the elements in a metric space
# as well as a distance metric for those elements.
#
class FeatureSpace:
    

    # Ths keeps track of the features that constitute this metric space.
    features = []  
    
    
    def __init__(self):
        self.features = []
        
    
    #
    # This method adds a new feature to this feature space. Each feature has a name
    # and a prototype. The prototype is used below when constructing a "blank"
    # element of this feature space.
    #        
    def AddFeature(self, name, proto,
                   metric=ManhattanDistance, 
                   remap=None, range=1.0, weight=1.0):
        
        f = {'name': name, 'proto': proto, 
             'metric': metric, 'remap': remap, 'range': range, 
             'weight': weight}
             
        self.features.append(f)

    
    #
    # This method computes the difference between two elements of 
    # this space. Each input is a dictionary. Presumably each dictionary
    # contains entries corresponding to the features of this space.
    #
    def Difference(self, aa, bb, get_metrics=False):
        
        # Get a list of scalar metric values for the features in this space.
        metrics = []
        weights = []
        
        for ff in self.features:
            featureName = ff['name']
            aaVal = aa[featureName]
            bbVal = bb[featureName]
            mm = ff['metric'](aaVal, bbVal)
            if ff['remap']:
                mm = ff['remap'](mm, ff['range'])
            metrics.append(mm)
            weights.append(ff['weight'])
        
        # Get a weighted sum of the metric values.
        mm = np.array(metrics)
        ww = np.array(weights)
        dd = sum(mm * ww) / sum(ww)

        if get_metrics:
            return dd, metrics
        else:
            return dd


    # 
    # This method returns a "blank" instance of an element of this 
    # space.
    #
    def Element(self):
        e = {}
        for ff in self.features:
            e[ff['name']] = ff['proto']
            
        return e



