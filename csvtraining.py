# fit a logistic regression on the training dataset
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
from sklearn.metrics import accuracy_score
import pandas
# create the inputs and outputs
file = pandas.read_csv('fakeDataSet.csv')
df = pandas.DataFrame(file)
data = [1,2,3,4]
emotion = [0]
dataDf = df[df.columns[data]]
emotionDf = df[df.columns[emotion]]

# define model
model = LogisticRegression(solver='lbfgs')
# fit model
model.fit(dataDf, emotionDf)
# make predictions
yhat = model.predict([[.6,.3,.2,.7]])
# evaluate predictions
print(yhat)
