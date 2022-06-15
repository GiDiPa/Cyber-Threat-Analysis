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

df2 = pd.read_csv("DS2/finalds2.csv")


#bit of Stats about categorical values
print(df2.head(10))
print(df2.describe())
#theCountry where the most number of malicious and benign are from created Datasets
print (df2[df2['Class']==0].groupby(['Country'])['Class'].value_counts().idxmax())
print (df2[df2['Class']==1].groupby(['Country'])['Class'].value_counts().idxmax())
#theOrganisation where the most number of malicious and benign are from created Datasets
#ASN not needed because it's representing the textual organisation
print (df2[df2['Class']==0].groupby(['Organisation'])['Class'].value_counts().idxmax())
print (df2[df2['Class']==1].groupby(['Organisation'])['Class'].value_counts().idxmax())
#most frequent TLD for corrispective classes
print (df2[df2['Class']==0].groupby(['TLD'])['Class'].value_counts().idxmax())
print (df2[df2['Class']==1].groupby(['TLD'])['Class'].value_counts().idxmax())


print(df2.head(10))
print(df2.describe())


missingList = df2.columns[df2.isna().any()].tolist()
for missing in missingList:
    if (missing == "Entropy"):
        df2['Entropy'] = df2['Entropy'].replace('?', np.nan).astype(float)
        df2['Entropy'] = df2['Entropy'].fillna(df2['Entropy'].max())
    elif (missing == 'IP'):
        df2['IP'].fillna('None', inplace = True)
    elif (missing == 'Country'):
        df2['Country'].fillna('None', inplace = True)
    elif (missing == 'City'):
        df2['City'].fillna('None', inplace = True)
    elif (missing == 'WhoisAge'):
        df2['WhoisAge'] = df2['WhoisAge'].fillna(df2['WhoisAge'].quantile(0.05))
    elif (missing == 'TLD'):
        df2['TLD'].fillna('None', inplace = True)
    elif (missing == 'ASN'):
        df2['ASN'].fillna('None', inplace = True)
        df2['ASN'] = df2['ASN'].astype(str)
    elif (missing == 'Organisation'):
        df2['Organisation'].fillna('None', inplace = True)
    elif (missing == '#SubDomains'):
        df2['#SubDomains'].fillna(0, inplace = True)



#see how data is distributed
#every type of histogram and boxplot would be saved as png. If
#don't want to save remove all lines with plt.savefig().


#split columns in two list: numerical values and categorical value
numerical = ['Entropy','WhoisAge','#SubDomains']
categorical = ['Online','Country','TLD','Organisation']
df2_plot = df2[numerical + categorical]


#histogram to see numbers of subDomains with colors
N, bins, patches = plt.hist(df2_plot['#SubDomains'], 30)
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



df2_plot[numerical].hist(bins=10, figsize=(15, 6), layout=(2, 2));
plt.show()

for column in categorical:
    ct = pd.crosstab(df2[column], df2['Class'])
    ct.plot(kind='line', stacked=True, color=['red','blue'], grid=False)
    plt.title(column + " X Type")
    #plt.savefig('img/' + column + 'Crosstab.png')
    plt.show()
    
for column in numerical:
    df2[column].hist(bins = 50)
    plt.title(column + " - Distribution")
    #plt.savefig('img/' + column + 'Histogram.png')
    plt.show(block = True)
    df2.boxplot(column = column)
    plt.title(column + " - Boxplot")
    #plt.savefig('img/' + column + 'Boxplot.png')
    plt.show(block=True)
    plt.interactive(False)
    ct = pd.crosstab(df2[column], df2['Class'])
    ct.plot(kind='line', stacked=True, color=['red','blue'], grid=False)
    plt.title(column + " X Type")
    #plt.savefig('img/' + column + 'Crosstab.png')
    plt.show()

#Transform Var WhoisAge applying logarithmic transformation

df2['WhoisAge'] = np.log(df2['WhoisAge']+1)#+1 to avoid 0 values.

#fit categorical data
varListFit = ['Domain','Online','IP','Country','City','TLD','Organisation']
le = LabelEncoder()
for i in varListFit:
    df2[i] = le.fit_transform(df2[i])

#split Datasets for training and test


train_set2 = df2.sample(frac=0.75, random_state=0)
test_set2 = df2.drop(train_set2.index)


#now passing to use prediction models giving the needed variables
#except for random forest predict model that will take every column



#in the classification model we prepare a table that contains all the 
#data about various classification models
# initialize list of lists 
resTable = [] 
name_model_for_ftable = ''  
# Create the pandas DataFrame 

#process of classification with ML
def classification_model(model,data, data_train, data_test, predictors, outcome):
    #fit the model
    model.fit(data_train[predictors], data_train[outcome])
    model.fit(data[predictors], data[outcome])

    t1=time()
    #Make predictions on training set:
    predictions = model.predict(data_test[predictors])
    
    #print accuracy and duration
    
    accuracy = metrics.accuracy_score(predictions, data_test[outcome])
    # Perform k-fold cross-validation with 5 folds
    kf=KFold(n_splits=4)
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
model = [DecisionTreeClassifier(max_depth=15), LogisticRegression(max_iter=1000),
    LinearSVC(dual=False),GaussianNB(),RandomForestClassifier(n_estimators=25, min_samples_split=25, max_depth=9, max_features=1)]


predictor_var = ['WhoisAge','Entropy','TLD','Online','#SubDomains']


'''
#Checking the best variables for random forest to avoid overfitting
predictor_varRF = ['Entropy','WhoisAge','Organisation','Online','Country','TLD','City','IP','#SubDomains']
model1 = RandomForestClassifier()
outcome = 'Class'
model1.fit(train_set2[predictor_varRF], train_set2[outcome])
featimp = pd.Series(model1.feature_importances_, index=predictor_varRF).sort_values(ascending=False)
print (featimp)
'''


for i in model:
    outcome_var = 'Class'
    name_model_for_ftable = type(i).__name__
    if (name_model_for_ftable == 'RandomForestClassifier'):
        predictor_var = ['Entropy','WhoisAge','Organisation','Online','IP']
    classification_model(i, df2, train_set2, test_set2, predictor_var, outcome_var)


'''
predictor_varRF = ['Entropy','WhoisAge','Organisation','Domain','TLD']
model1 = RandomForestClassifier()
outcome = 'Class'
model1.fit(train_set1[predictor_varRF], train_set1[outcome])
featimp = pd.Series(model1.feature_importances_, index=predictor_varRF).sort_values(ascending=False)
print (featimp)


'''