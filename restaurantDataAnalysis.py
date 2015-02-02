import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

restData=pd.read_csv('RestaurantResults.csv')
income=pd.read_csv('irsIncome.csv')


#camis is a unique identifier for the restaurant (because there are lots of Wendy's)
i=0
scores=[]
boroMice={'MANHATTAN':[0,0],'BROOKLYN':[0,0],'QUEENS':[0,0],'STATEN ISLAND':[0,0],'BRONX':[0,0]}
boros=[]
zips=[]
numgroups=0
globalMaxScore=0
for name,group in restData.groupby('CAMIS'):
    #myname,mygroup=name,group
    violations=set(group['VIOLATION CODE'].values)
    zipcode=group['ZIPCODE'].max()
    maxScore=group['SCORE'].max()
    boro=group['BORO'].mode().values
    if(maxScore>=0 and zipcode>10000 and len(boro)>0 and not boro==['Missing']): #only remember the ones with actual scores
        scores.append(maxScore)
        zips.append(zipcode)
        numgroups+=1
        boros.append(boro[0])
        boroMice[boro[0]][1]+=1
        if('04L' in violations):
            boroMice[boro[0]][0]+=1           
    if(maxScore>globalMaxScore):
        globalMaxScore=maxScore
        dirtiest=group['DBA'].mode()
        

zipcodeset=set(zips)
zips=np.array(zips)
boros=np.array(boros)
scores=np.array(scores)
numPerZip=[]
avgzipdata=[]

for zipcode in zipcodeset:
    zipdata=scores[zips==zipcode]
    boro=boros[zips==zipcode][0]
    avgzipdata.append([np.mean(zipdata),int(zipcode),boro])

#print avgzipdata[0:5]


incomeDist=[]
zipcodeIncomeScore=[]
for zipcode in zipcodeset:
    incomeBins=income[income['zipcode']==zipcode]['A00100'].values
    numreturns=sum(income[income['zipcode']==zipcode]['N1'].values)
    if len(incomeBins)==0: #no income information
        pass
    else:
        #print zipcode, incomeBins, len(incomeBins)
        boro=boros[zips==zipcode][0]
        incomeDist.append([zipcode,incomeBins])
        #zipcode, fraction in lowest bracket, avg score, boro
        zipcodeIncomeScore.append([zipcode,incomeBins[0]/sum(incomeBins),np.mean(scores[zips==zipcode]),boro])

#plot the average score vs percent in lowest bracket

percentPoor=[a[1] for a in zipcodeIncomeScore]
avgScore=[a[2] for a in zipcodeIncomeScore]
plt.figure()
[m,b]=np.polyfit(percentPoor,avgScore,1)
x=np.linspace(0,max(percentPoor),300)
y=m*x+b
colors=['r','g','b','m','y']
plt.plot(x,y,label='Linear Fit, (slope is '+"{:.2f}".format(m)+')')
boroNames=set(['MANHATTAN','BROOKLYN','BRONX','QUEENS','STATEN ISLAND'])

plt.annotate(s='a \"filthy\"\n rich zipcode', xy=(.0300127,51.5),xytext=(.08,51),arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc,angleA=50,armA=20,angleB=-50,armB=20,rad=9"))
for ind,boro in enumerate(boroNames):
    percentPoor=[a[1] for a in zipcodeIncomeScore if a[3]==boro ]
    avgScore=[a[2] for a in zipcodeIncomeScore if a[3]==boro ]
    plt.plot(percentPoor,avgScore,'.',markersize=15,label=boro, color=colors[ind])

plt.ylabel('Average Restaurant Violation Score')
plt.xlabel('Percent of Population in the Lowest Income Bracket')
plt.title('Restaurant Health Violation Score vs Income by Zipcode')

plt.legend()
plt.show()

#make a histogram of all possible scores
plt.figure()
restData['SCORE'].hist(bins=157)
plt.xlim([-1,156])
plt.xlabel('Violation Score (0 means no violations)')
plt.ylabel('Number of Occurrences')
plt.show()

percentMice=[]
for boro in boroNames:
    percentMice.append(boroMice[boro][0]/float(boroMice[boro][1]))

#make a bar plot of percentage of restaurants with mice infestations in each boro
plt.figure()
ind=np.arange(5)
plt.bar(ind,percentMice,width=.5,color=colors,align='center')
plt.ylabel('Fraction of Restaurants with Mice Infestations')
plt.xticks(ind,tuple(boroNames))
plt.xlim([-.5,4.5])
plt.show()
