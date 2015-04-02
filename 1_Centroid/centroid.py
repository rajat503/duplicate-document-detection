import sys
import math
import operator
f = open('tf.txt', 'r')
values=[]
similar=[]
centroid_list=[]
for line in f:
	centroid=0
	values=line.split('), (')
	values[0]=values[0].replace('[(','')
	values[len(values)-1]=values[len(values)-1].replace(')]','')
	for i in values:
		centroid += float(i.split(', ')[1])
	centroid=centroid/len(values)
	first=2
	second=2
	third=2
	for i in values:
		diff=abs(centroid-float(i.split(', ')[1]))
		if diff<=first:
			first=diff
	for i in values:
		diff=abs(centroid-float(i.split(', ')[1]))
		if diff>first and diff<second:
			second=diff
	for i in values:
		diff=abs(centroid-float(i.split(', ')[1]))
		if diff>first and diff>second and diff<third:
			third=diff
	similar.append([first,second,third])
	# 	print len(values)
	centroid_list.append(centroid)
# for i in range(len(centroid_list)):
# 	print i+1, centroid_list[i]
cosine_list=[]
for j in range(len(similar)-1):
	for k in range(j+1,len(similar)):
		cosine=0
		for i in range(3):
			cosine += similar[j][i]*similar[k][i]
		cosine=cosine/math.sqrt(similar[j][0]*similar[j][0]+similar[j][1]*similar[j][1]+similar[j][2]*similar[j][2])
		cosine=cosine/math.sqrt(similar[k][0]*similar[k][0]+similar[k][1]*similar[k][1]+similar[k][2]*similar[k][2])
		cosine_list.append([cosine,j,k])
cosine_list=sorted(cosine_list, key=operator.itemgetter(0), reverse=True)
for i in range(5):
	print cosine_list[i]


