#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:54:24 2023

@author: vboxuser
"""

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import sys


# host_name = sys.argv[1]
# port_nb = sys.argv[2]


sc = SparkContext()
ssc = StreamingContext(sc, 15)

# print(port_nb)

lines = ssc.socketTextStream('localhost',1337)

# # Solution 1
# counts_total = lines\
#     .map(lambda line: line.split("\t"))\
#     .map(lambda url: ((url[0], url[1]), 1))\
#     .reduceByKeyAndWindow(func=lambda a, b: a+b, invFunc=lambda a, b: a-b, windowDuration=60)

# filter_count = counts_total.filter(lambda pair : pair[1] > 2)

# filter_count.pprint()

# Solution 2
# counts_unique = lines.map(lambda line: line.split("\t")).map(lambda url: ((url[0], url[1]), 1)).reduceByKeyAndWindow(func=lambda a, b: a+b, invFunc=None, windowDuration=60).reduceByKey(lambda a, b : a[0]+b)

# Solution 3
# counts_unique = lines.map(lambda line: line.split("\t")).map(lambda url: ((url[0], url[1]), 1)).countByValueAndWindow(windowDuration=60, slideDuration=15)

# # Solution 4
# counts_total = lines.map(lambda line: line.split("\t"))
    # .map(lambda url: ((url[0], url[1]), 1))\
    # .reduceByKey(func=lambda a, b: a)\
    # .map(lambda url : (url[0][1], url[1]))\
    # .reduceByKeyAndWindow(func = lambda a, b :a+b, invFunc=None, windowDuration=60)



# counts_sorted = counts_total.transform(
#     lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))

# counts_filtered = counts_sorted.filter(lambda pair : pair[1] >= 5)

lines.pprint()

# counts_sorted = counts.transform(lambda rdd: rdd)

# counts_sorted.pprint()

# filter_count = counts_sorted.filter(lambda pair : pair[1] >2)


# counts_txt = counts_sorted.saveAsTextFiles("/home/vboxuser/Documents/results")

# counts_sorted.pprint()

ssc.start()
ssc.awaitTermination()