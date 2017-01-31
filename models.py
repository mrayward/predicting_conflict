from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import precision_recall_fscore_support


#independent variables
al = pd.read_csv('al.csv')

#dependent variable
target = pd.read_csv('target.csv')
target = target.drop('Unnamed: 0', axis = 1)

#train test split
train = al[al['year']< 2000]
test = al[al['year']>=2000]
y_train = train['civtot']
x_train = train.drop(['civtot', 'inttot'], axis =1)
y_test = test['civtot']
x_test = test.drop(['civtot', 'inttot'], axis =1)

#model
def cross_val_score(model, x_train, y_train, cv=10):
    score = cross_val_score(clf, x_train, y_train, cv=10)
    return score

def fit(model, x_train, y_train):
    fit = model.fit(x_train, y_train)

def score(model, x_test, y_test):
    score = clf.score(x_test, y_test)
    print 'Model {0} score: {1}'.format(model, score)
    return score

def precision_recall_fscore(model, y_true, y_pred, average = 'macro'):
    prec_rec_fsc= precision_recall_fscore_support(y_true, y_pred, average='macro')
    print 'Model {0} precision, recall, fscore: {1}'.format(model, prec_rec_fsc)



if __name__ == "__main__":
    #Model 1- Decision Tree Classifier
    dec_tree = DecisionTreeClassifier(random_state=random_state)
    cross_val_score(dec_tree, x_train, y_train, cv=10)
    fit(dec_tree, x_train, y_train)
    score(dec_tree, x_test, y_test)
    y_pred = dec_tree.predict(x_test)
    precision_recall_fscore(dec_tree, y_test, y_pred)
    #Model 2 - Random Forest Classifier
    rf = RandomForestClassifier()
    cross_val_score(rf, x_train, y_train, cv=10)
    fit(rf, x_train, y_train)
    score(clf, x_test, y_test)
    y_pr = rf.predict(x_test)
    precision_recall_fscore(rf, y_test, y_pr)
