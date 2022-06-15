import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib import pyplot as plt
import seaborn as sns
import re
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, export_graphviz
#from sklearn.svm import SVC -- This is a problem to use with big datasets
from sklearn.svm import LinearSVC
from sklearn.model_selection import KFold
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from time import time

df1 = pd.read_csv("DS1/finalds1.csv")

print(df1.head(10))
print(df1.describe())

'''
#theCountry where the most number of malicious and benign are from created Datasets
print (df1[df1['Class']==0].groupby(['Country'])['Class'].value_counts().idxmax())
print (df1[df1['Class']==1].groupby(['Country'])['Class'].value_counts().idxmax())
#theOrganisation where the most number of malicious and benign are from created Datasets
#ASN not needed because it's representing the textual organisation
print (df1[df1['Class']==0].groupby(['Organisation'])['Class'].value_counts().idxmax())
print (df1[df1['Class']==1].groupby(['Organisation'])['Class'].value_counts().idxmax())
#most frequent TLD for corrispective classes
print (df1[df1['Class']==0].groupby(['TLD'])['Class'].value_counts().idxmax())
print (df1[df1['Class']==1].groupby(['TLD'])['Class'].value_counts().idxmax())
'''

missingList = df1.columns[df1.isna().any()].tolist()
for missing in missingList:
    if (missing == "Entropy"):
        df1['Entropy'] = df1['Entropy'].replace('?', np.nan).astype(float)
        df1['Entropy'] = df1['Entropy'].fillna(df1['Entropy'].max())
    elif (missing == 'IP'):
        df1['IP'].fillna('None', inplace = True)
    elif (missing == 'Country'):
        df1['Country'].fillna('None', inplace = True)
    elif (missing == 'City'):
        df1['City'].fillna('None', inplace = True)
    elif (missing == 'WhoisAge'):
        df1['WhoisAge'] = df1['WhoisAge'].fillna(df1['WhoisAge'].quantile(0.10))
    elif (missing == 'TLD'):
        df1['TLD'].fillna('None', inplace = True)
    elif (missing == 'ASN'):
        df1['ASN'].fillna('None', inplace = True)
        df1['ASN'] = df1['ASN'].astype(str)
    elif (missing == 'Organisation'):
        df1['Organisation'].fillna('None', inplace = True)
    elif (missing == '#SubDomains'):
        df1['#SubDomains'].fillna(0, inplace = True)
    
#print(df1.describe())
#print(df1.head(10))


#see how data is distributed
#every type of histogram and boxplot would be saved as png. If
#don't want to save remove all lines with plt.savefig().


#split columns in two list: numerical values and categorical value
#just for analysis purpose
numerical = ['Entropy','WhoisAge','#SubDomains']
categorical = ['Online','Country','TLD','Organisation']
df1_plot = df1[numerical + categorical]

'''
#histogram to see numbers of subDomains with colors
N, bins, patches = plt.hist(df1_plot['#SubDomains'], 30)
cmap = plt.get_cmap('jet')
low = cmap(0.5)
medium =cmap(0.2)
high = cmap(0.7)
for i in range(0,2):
    patches[i].set_facecolor(low)
for i in range(2,4):
    patches[i].set_facecolor(medium)
for i in range(4,20):
    patches[i].set_facecolor(high)
plt.xlabel("#SubDomains", fontsize=16)  
plt.ylabel("Records", fontsize=16)
plt.xticks(fontsize=14)  
plt.yticks(fontsize=14)

plt.show()



df1_plot[numerical].hist(bins=10, figsize=(15, 6), layout=(2, 2));
plt.show()

for column in categorical:
    ct = pd.crosstab(df1[column], df1['Class'])
    ct.plot(kind='line', stacked=True, color=['red','blue'], grid=False)
    plt.title(column + " X Type")
    #plt.savefig('img/' + column + 'Crosstab.png')
    plt.show()
    
for column in numerical:
    df1[column].hist(bins = 50)
    plt.title(column + " - Distribution")
    #plt.savefig('img/' + column + 'Histogram.png')
    plt.show(block = True)
    df1.boxplot(column = column)
    plt.title(column + " - Boxplot")
    #plt.savefig('img/' + column + 'Boxplot.png')
    plt.show(block=True)
    plt.interactive(False)
    ct = pd.crosstab(df1[column], df1['Class'])
    ct.plot(kind='line', stacked=True, color=['red','blue'], grid=False)
    plt.title(column + " X Type")
    #plt.savefig('img/' + column + 'Crosstab.png')
    plt.show()
'''


#Transform Var WhoisAge applying logarithmic transformation

df1['WhoisAge'] = np.log(df1['WhoisAge']+1)#+1 to avoid 0 values.


#fit categorical data
varListFit = ['Domain','Online','IP','Country','City','TLD','Organisation','ASN']
le = LabelEncoder()
for i in varListFit:
    df1[i] = le.fit_transform(df1[i])

#split Datasets for training and test



train_set1 = df1.sample(frac=0.6, random_state=0)
test_set1 = df1.drop(train_set1.index)


#now passing to use prediction models giving the needed variables
#except for random forest predict model that will take every column



#in the classification model we prepare a table that contains all the 
#data about various classification models
# initialize list of lists 
resTable = [] 
name_model_for_ftable = ''  
# Create the pandas DataFrame 

#process of classification with ML
def classification_model(model, data, data_train, data_test, predictors, outcome):
    #fit the model
    model.fit(data_train[predictors], data_train[outcome])
    model.fit(data[predictors], data[outcome])

    t1=time()
    #Make predictions on training set:
    predictions = model.predict(data_test[predictors])
    
    #print accuracy and duration
    
    accuracy = metrics.accuracy_score(predictions, data_test[outcome])
    # Perform k-fold cross-validation with 5 folds
    kf=KFold(n_splits=3)
    pred=[]
    for train, test in kf.split(data):
        # Filter training data
        train_predictors =(data_train[predictors])
        # The target we're using to train the algorithm.
        train_target = data_train[outcome]
        # Training the algorithm using the predictors and target.
        model.fit(train_predictors, train_target)
        # Record error from each cross-validation run
        pred.append(model.score(data_test[predictors], data_test[outcome]))
    f_report = metrics.f1_score(data_test[outcome], predictions, average = 'macro')
    dur = round(time()-t1, 3)
    tempA = "%s" % "{0:.3%}".format(accuracy)
    tempB = str(dur) + 's'
    print("Accuracy : %s" % "{0:.3%}".format(accuracy) + ' || ' + "Cross-Validation Score : %s" % "{0:.3%}".format(np.mean(pred)) + ' || ' + "F-Score: " + str(f_report) + ' || ' + "Duration: " + tempB)
    #fit the model again so that it can be referred outside the function:
    model.fit(data_train[predictors], data_train[outcome])
    model.fit(data[predictors], data[outcome])


#now we use various model of prediction to see performances and results
#each model has is own setup after several tests to get the better values.
model = [DecisionTreeClassifier(max_depth=15), LogisticRegression(max_iter=105),#max iteration: default is 100, with minimum 105 value I avoid the reach limit.
    LinearSVC(dual=False),GaussianNB(),RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=9, max_features=1)]


predictor_var = ['Online','WhoisAge','#SubDomains','Organisation','Entropy','TLD']


'''
#Checking the best variables for random forest to avoid overfitting
predictor_varRF = ['Entropy','WhoisAge','Organisation','Online','Country','TLD','City','IP','#SubDomains']
model1 = RandomForestClassifier()
outcome = 'Class'
model1.fit(train_set1[predictor_varRF], train_set1[outcome])
featimp = pd.Series(model1.feature_importances_, index=predictor_varRF).sort_values(ascending=False)
print (featimp)
'''


for i in model:
    outcome_var = 'Class'
    name_model_for_ftable = type(i).__name__
    if (name_model_for_ftable == 'RandomForestClassifier'):
        predictor_var = ['Entropy','WhoisAge','Organisation','IP','TLD']#these are the best five for RandomForestClassifier
    classification_model(i, df1, train_set1, test_set1,  predictor_var, outcome_var)

