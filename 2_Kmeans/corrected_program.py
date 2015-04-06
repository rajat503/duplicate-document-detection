import sys
import math
from scipy.cluster.vq import kmeans2
import numpy as np

number_of_clusters=10
f=open('termid.txt','r')
word_list=[]

#extracting all words and their id from termid.txt to a list
for line in f:
	word_bracket=line.split(', u\'')
	for j in word_bracket:
		word_list.append(j.split('\': '))
word_list.remove([''])
f.close()

# generating keywords vectors of tf values and making a list of the vectors 
keyword_vector=[]
for i in word_list:
	current_keyword_vector=[]
	f=open('tf.txt','r')
	for line in f:
		values=line.split('), (')
		values[0]=values[0].replace('[(','')
		values[len(values)-1]=values[len(values)-1].replace(')]','')
		tf_to_add=0.0
		for j in values:
			current_tf=float(j.split(', ')[1])
			if j.split(', ')[0] == i[1]:
				tf_to_add=current_tf
				break
		current_keyword_vector.append(tf_to_add)
	keyword_vector.append(current_keyword_vector)
	f.close()
X=np.array(keyword_vector)
centroid, labels = kmeans2(X, number_of_clusters, iter=10, thresh=1e-05, minit='random', missing='warn')

selected_vectors=[]
features_selected=[]
for i in range(number_of_clusters):
	smallest_vector=[]
	min_distance=5000
	min_j=0
	for j in range(len(labels)):
		if labels[j]==i:
			calculated_distance=np.linalg.norm(np.array(centroid[i])-np.array(keyword_vector[j]))
			if calculated_distance < min_distance:
				min_distance = calculated_distance
				smallest_vector = keyword_vector[j]
				min_j=j
	selected_vectors.append(smallest_vector)
	features_selected.append(word_list[min_j][0])
for i in features_selected:
	print i