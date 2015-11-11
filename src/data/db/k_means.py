import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn import datasets

x = []
y = []
with open('abl_data.csv') as csvfile:
# with open('vxy_data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	# x+=[[row['x_relative'],row['y_relative'],row['z_relative']]]
    	# x+=[[row['z_relative']]]
    	# x += [[row['index_z'],row['middle_z'],row['ring_z']]]   ##xvw
    	x += [[row['thumb_z'],row['middle_z']]] ###abl
    	y+=[row['lable']]	

# print y

est = KMeans(n_clusters=3)
est.fit(x)
print est
print est.cluster_centers_
i =0
# error = 0
for p in est.labels_:
	print str(y[i])
	print p
	# error+=1
	i+=1
# print error
# print est.labels_
