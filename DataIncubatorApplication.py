import pandas as pd
import numpy as np

hits=pd.read_csv('hits.csv')

users=set(hits['user'])
avgPgPerUser=len(hits)/float(len(users))
print "Average number of pages visited: ", avgPgPerUser
#histogram of frequency of number of hits per user
usersAndPageHits=hits['user'].value_counts()
#subset of those who visited more than once
returningUsers=usersAndPageHits[usersAndPageHits>1]
numHitsfromReturning=sum(returningUsers)
avgHitsfromReturning=numHitsfromReturning/float(len(returningUsers))
print "Average number of pages visited from those that visited twice or more: ", avgHitsfromReturning


#bit of nonsense
hits.groupby('user').sum().mean()


for name,group in hits.groupBy('user'):
    numgroups+=1