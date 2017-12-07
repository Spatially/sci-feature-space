# sci-feature-space

This repository contains a python moduled named "miff" that lets you define a 
multivariate feature space, and compute a distance
metric between its elements.

A "feature space" as defined in this module is just a set of individual features, which
each may be real/integer/categorical/boolean and scalar/vector valued. So for example
you could have a feature space describing census blocks, where each element of the space
consists of the name of the town it falls into, its area in square kilometers, the income
distribution of its inhabitants, and the median age of all residents. There is no limit to the
Number of features that can be defined for a feature space.

This module then provides a flexible framework for computing scalar distance metrics for the
elements of this feature space. The general approach is that each individual feature
is associated with a method for computing a scalar distance metric for that feature individually.
You can choose between several different per-feature distance metrics (e.g. manhattan distance,
cosine distance, etc.) or define your own.

This module then provides routines for scaling the per-feature distance metrics to a comparable
range. For example if a feature space contains both median age and median income (in dollars),
the individual differences are not really comparable: an age difference of 50 years is
probably a lot more significant than an income difference of 50 dollars. So this module contains
a choice of methods that can be used to map per-feature difference values into the range
[0 1] so that they are more directly comparable.

This module combines the re-mapped metric values using a simple weighted sum. The weights
are user-defined.



