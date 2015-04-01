import sys
import math
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

def do_k_mean(x):
	X = np.array(zip(x,np.zeros(len(x))), dtype=np.int)
	bandwidth = estimate_bandwidth(X, quantile=0.003)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(X)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_
	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)
	cluster_list=[]
	for k in range(n_clusters_):
		my_members = labels == k # print "cluster {0}: {1}".format(k, X[my_members, 0])
		cluster_list.append(X[my_members, 0])
	return cluster_list


f=open('tf.txt','r')
randomnumbers=open('randomnumbers.txt','r')
values=[]
x=[]
y=[]
for line in f:
	values=line.split('), (')
	values[0]=values[0].replace('[(','')
	values[len(values)-1]=values[len(values)-1].replace(')]','')
	for i in values:
		y.append(int(i.split(', ')[0]))
		x.append(int(float(i.split(', ')[1])*10000000000))

after_clustering=do_k_mean(x)
centroid_list=[]
for i in after_clustering:
	# print i
	centroid=0
	for j in i:
		centroid+= j
	if len(i)==0:
		continue
	centroid=centroid/len(i)
	centroid_list.append(centroid)
best_tfidf=[]
co=0
for i in after_clustering:
	first=10000000000
	if(len(i)!=0):
		for j in i:
			diff=abs(centroid_list[co]-j)
			if diff<=first:
				first=diff
				minimum=j
		co+=1
		best_tfidf.append(minimum)
# for i in best_tfidf:
# 	print i
f.close()
features_serial=[]
for i in best_tfidf:
	for j in range(len(x)):
		# print "x % i %", (x[j], i)
		if x[j]==i:
			# print "x "+x[j]
			# print "i"+i
			features_serial.append(y[j])
			break
f=open('termid.txt','r')
word_list=[]
word_list_serial=[]
final_words=[]
for line in f:
	word_raw=line.split(', u\'')
	for j in word_raw:
		word_list.append(j.split('\': '))
for i in features_serial:
	for j in word_list:
		if j[-1]==str(i):
			final_words.append(j[0])
			break
for i in final_words:
	print i