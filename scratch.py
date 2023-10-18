import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

attributes = np.array(['Crossing','Finishing','Heading Accuracy','Short Passing','Volleys','Dribbling','Curve','FK Accuracy',
            'Long Passing','Ball Control','Acceleration','Sprint Speed','Agility','Reactions','Balance','Shot Power',
            'Jumping','Stamina','Strength','Long Shots','Aggression','Interceptions','Positioning','Vision','Penalties',
            'Composure','Defensive Awareness','Standing Tackle','Sliding Tackle','GK Diving','GK Handling','GK Kicking', # edit 1
            'GK Positioning','GK Reflexes'])

cluster = np.array([[-0.16576781, 4.07675775, 1, 2],
 [ 9.60287845, -4.7550837, 3, 4],
 [-4.91148837,  4.91774862, 5, 6],
 [ 6.09044751,  3.04444992, 7, 8],
 [-9.45897178,  1.35667948, 9, 10]])


print(cluster[:, [0, 2,3]])
closest, _ = pairwise_distances_argmin_min([[0, 1, 2]], cluster[:, [0, 2,3]])
print(closest)

#print(attributes[:, [0, 11, 19, 20, 1, 30]]) [[45, 55, 35, 40, 50, 15]]

centers2 = centers[:, [0, 11, 19, 20, 1, 30]]
closest, _ = pairwise_distances_argmin_min([[45, 55, 35, 40, 50, 15]], centers2)
