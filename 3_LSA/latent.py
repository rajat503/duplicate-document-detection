
from scipy import linalg,array,dot,mat,transpose
from math import *
from pprint import pprint
import sys
from scipy.cluster.vq import kmeans2
import numpy as np

  
class LSA:
  
  
    def __init__(self, matrix, termslabel,docslabel):

        self.matrix = array(matrix)
        self.termslabel = termslabel
        self.docslabel = docslabel
  
    
  
    def lsaTransform(self,k=2):
       
        rows,cols= self.matrix.shape

        if k < rows: #Its a valid reduction
  
            #Sigma comes out as a list rather than a matrix
            s,sigma,ut = linalg.svd(self.matrix)
      
            #Dimension reduction, build SIGMA'
            sigmak = linalg.diagsvd(sigma[:k],k,k)
            sk = transpose(transpose(s)[:k])
            utk = ut[:k] 
            #print utk
            #print sk.shape
            #print utk.shape

            return( dot(sk,sigmak), transpose(dot(sigmak,utk)))



if __name__ == '__main__':
  
   
    # f=open('Matrix.txt','r')
    # matrix=[]

    # for j in f:
    #     matrix.append(j)

    number_of_clusters=10
    f=open('termid.txt','r')
    word_list=[]

    #extracting all words and their id from termid.txt to a list
    for line in f:
        word_bracket=line.split(', u\'')
        for j in word_bracket:
            word_list.append(j.split('\': '))
            #word_list.remove([''])

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
                if j.split(', ')[0] == i[-1]:
                    tf_to_add=current_tf
                    break
            current_keyword_vector.append(tf_to_add)
        keyword_vector.append(current_keyword_vector)
        f.close()



    X=np.array(keyword_vector)

    docslabel=[str(i) for i in xrange(60)]

    lsa = LSA(X,word_list, docslabel)
    
    terms,docs = lsa.lsaTransform(60)
    # for i in terms:
    #     print i


    centroid, labels = kmeans2(terms, number_of_clusters, iter=10, thresh=1e-05, minit='random', missing='warn')

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