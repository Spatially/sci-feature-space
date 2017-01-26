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

This module combines the re-mapped metric values using a sinmple weighted sum. The weights
are user-defined.



# Spatial Signature Difference Calculation

For several planned Latitude / Gravity product features, there is a need to quantify the difference between spatial signatures for a pair of locations. A _spatial signature_ is an arbitrary collection of features of a variety of types (scalar, vector, categorical, and so on). Because of the number and variety of features that may compose a spatial signature, there is no simple definition of their difference that is generally applicable. 

Nonetheless, the science team has been developing methods to quantify spatial signautre differences. The approach is based on aggregating feature-by-feature difference metrics in a variety of ways. The specifics for any given situation will be the subject of ongoing analysis by the science team. Since the results of these analyses need to be communicated to the engineering team for implementation in Latitude / Gravity, there is a need for a clear specification of the general form of spatial signautre difference calculations. This document is an attempt to provide such a specification. 

### General approach
A _spatial signature_ is a collection of features describing attributes of a location that are relevant for a given analysis.  Notationally, a spatial signature $X(g)$ for some geospatial location $g$ is $X(g) \equiv \{x_1(g),x_2(g),...x_n(g)\}$, where each $x_i(g)$ represents some feature referenced to location $g$, such as local population density, distance to the nearest hospital, and so on. In the notation that follows, the $(g)$ parameter will be omitted for readability. Spatial signatures for different locations will be denoted by capital letters like $X$ and $Y$, and their component features will be denoted by lowercase letters like $x_i$ and $y_i$.

The approach to computing signature differences is to first compute difference metrics for the component features individually.  So given two spatial signatures $X$ and $Y$, one computes $\{d_1(x_1,y_1), ..., d_n(x_n,y_n)\}$. A final difference metric for the signatures $d(X,Y)$ involves aggregating these per-feature metrics into a single scalar value. 

This approach has to deal with several issues.

 - _An appropriate mathematical form must be chosen to compute each $d_i$._ For any given feature, certain forms may be particularly appropriate, while others may not be applicable at all. 
 - _There is a need to scale the $d_i$ into a comparable dynamic range._ For example one feature may represent population while another represents a count of business types. The former would typically have a wider dynamic range than the latter. 
 - _There is a need to weight the contributions of the individual $d_i$ to the overall result._ For a particular application, some of the $d_i$ may be deemed more important than others. 
 - _There are a number different mathematical approaches that could be used to aggregate the $d_i$. _

The sections below elaborate on these points.

### Per-feature difference metrics

This section presents several approaches that may be used to compute differences on a feature-by-feature basis. Many more methods exist, and may prove to be useful for certain analyses. But this section presents a minimal set that of metrics that will probably be used frequently.

In this section, a pair of features will be denoted $x$ and $y$. If the features are vector-valued, the component values will be denoted by subscripts, e.g. $x_i$ or $y_i$. 

For some features, the only relevant factor in difference calculations is whether $x$ and $y$ have the same value. For example, this is appropriate for categorical data: either two instances have the same category or they have different categories. Then a simple metric is the _discrete distance_, defined as

$$d(x,y) = \cases{0 &  \text{if } x = y \cr1 &\text{otherwise.}}$$

For real-valued scalars, an appropriate distance metric is simply the absolute value of the difference.

$$d(x,y)=|x-y|$$

For features that are real-valued vectors $x_i =[ x_1,x_2,...,x_m]$ and $y =[ y_1,y_2,...,y_m]$, other metrics include the Euclidean distance

$$d(x,y) = \root \of {\sum_{i=1}^n (x_i - y_i)^2}$$

and the Manhattan distance

$$d(x,y) = \sum_{i=1}^n |x_i - y_i|$$

A metric that may be relevant for some applications is the _cosine distance_, which for a pair of $m$-dimensional vectors $x$ and $y$ is defined as

$$d(x,y) = \frac{x \cdot y}{|x||y|}.$$

This quantity is essentially the cosine of the angle between the two vectors in $m$-dimensional Euclidean space. It is a useful quantity if the _relative_ magnitudes of the vector components are relevant, but their _absolute_ magnitudes are not. 

A number of possible features are essentially distributions of some quantity over a range of bins. Examples are distributions of ages or incomes, which are typically reported in some small number of categories. For features of this type, an appropriate metric is the Hellinger distance.

$$d(x,y) = \root \of { 1 - \sum_{i=1}^m \root \of {x_i y_i}}$$

This quantity takes on a value of zero if two distributions are identical.

### Scaling per-feature difference metrics
As noted above, different per-feature metrics may yield different $d_i$ values having incomparable dynamic ranges. One approach to dealing with this problem is to map all per-feature differences into the range $[0, 1]$. That is, an originally computed distance $d_i$ for feature $i$ is replaced by a value $d'_i={\frak M}(d|r)$, where $\frak M$ is a function ${\frak M}:[0,\infty) \rightarrow [0,1]$ given some chosen range parameter $r$. One possibility is a linear mapping

$${\frak M}(d|r)=\min[d/r , 1]$$

where $r \gt 0$ is a range parameter chosen for the particular feature. This equation scales the original distances up to $r$ to the range $[0, 1]$, with larger distances being mapped to $1$. While such a mapping can put disparate features onto a comparable measurement scale, it has the drawback of providing no distinction between distances beyond the arbitrarily chosen range parameter. An alternative is an exponential remapping.

$${\frak M} (d | r) = 1 - e^{-d/r},$$

which maps all values into the range $[0,1)$

### Aggregating per-feature metrics

For many purposes it will be necessary to aggregate the scaled per-feature metrics into a single scalar value $d(X,Y)$ for a pair of signatures $X$ and $Y$. This is necessary, for example, when ranking a number of locations according to their similarity to a location of interest. The simplest approach is to apply a weighted linear sum.

$$d(X,Y) = \sum_{i=1}^n w_i d'_i,$$

where the $w_i$ are weights that represent the relative importance of feature $i$ for the overall analysis. 

The weighted sum is essentially an $L_1$ norm, like the Manhattan distance. Another choice is to use an $L_2$ norm analogous to the Euclidean distance.

$$d(X,Y) = \root \of { \sum_{i=1}^n w_i {d'_i}^2 } $$

### Summary

The descriptions given above constitute a general approach to defining spatial signature differences. If the science team decides on the specifics for a particular analysis problem, this result will be communicated to the engineering team using the concepts and terminology described above. 

For example, suppose one is dealing with a spatial signature whose features include the local population, the income distribution of that population, and the number of coffee shops with 1 mile. Analysis may show that for a given problem the best definition of a spatial signature difference uses the following parameters.

| Feature| Difference Metric | Scaling | Range | Weight
|--|--|--|
| population| scalar| exponential | 1000 | 0.3
| income distribution | hellinger| none| n/a | 0.5
| coffee shops| scalar| linear| 5 | 0.2
| aggregation method: | $L_1$ norm

This constitutes a full specification of how differences should be computed for these features.  In any case, if other per-feature metrics or aggregation approaches are deemed necessary for a given analysis, these should be communicated to the engineering team as needed.