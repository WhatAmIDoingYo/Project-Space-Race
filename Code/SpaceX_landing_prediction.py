import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

# Function to plot confusion matrix
def plot_confusion_matrix(y, y_predict):
    cm = confusion_matrix(y, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

# Load the data
URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
data = pd.read_csv(URL1)

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
X = pd.read_csv(URL2)

# Create target variable Y
Y = data['Class'].to_numpy()

# Standardize the features
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Logistic Regression with GridSearchCV
parameters_lr = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters_lr, cv=10)
logreg_cv.fit(X_train, Y_train)
print("Logistic Regression - Best parameters:", logreg_cv.best_params_)
print("Logistic Regression - Best score:", logreg_cv.best_score_)

logreg_test_accuracy = logreg_cv.score(X_test, Y_test)
print("Logistic Regression - Test Accuracy:", logreg_test_accuracy)

yhat_lr = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_lr)

# SVM with GridSearchCV
parameters_svm = {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
                  'C': np.logspace(-3, 3, 5),
                  'gamma': np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters_svm, cv=10)
svm_cv.fit(X_train, Y_train)
print("SVM - Best parameters:", svm_cv.best_params_)
print("SVM - Best score:", svm_cv.best_score_)

svm_test_accuracy = svm_cv.score(X_test, Y_test)
print("SVM - Test Accuracy:", svm_test_accuracy)

yhat_svm = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_svm)

# Decision Tree with GridSearchCV
parameters_tree = {'criterion': ['gini', 'entropy'],
                   'splitter': ['best', 'random'],
                   'max_depth': [2*n for n in range(1,10)],
                   'max_features': ['sqrt'],  # Replaced 'auto' with 'sqrt' to avoid deprecation warning
                   'min_samples_leaf': [1, 2, 4],
                   'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters_tree, cv=10)
tree_cv.fit(X_train, Y_train)
print("Decision Tree - Best parameters:", tree_cv.best_params_)
print("Decision Tree - Best score:", tree_cv.best_score_)

tree_test_accuracy = tree_cv.score(X_test, Y_test)
print("Decision Tree - Test Accuracy:", tree_test_accuracy)

yhat_tree = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_tree)

# KNN with GridSearchCV
parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                  'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                  'p': [1, 2]}
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN, parameters_knn, cv=10)
knn_cv.fit(X_train, Y_train)
print("KNN - Best parameters:", knn_cv.best_params_)
print("KNN - Best score:", knn_cv.best_score_)

knn_test_accuracy = knn_cv.score(X_test, Y_test)
print("KNN - Test Accuracy:", knn_test_accuracy)

yhat_knn = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat_knn)

# Compare the models
accuracies = {
    'Logistic Regression': logreg_test_accuracy,
    'SVM': svm_test_accuracy,
    'Decision Tree': tree_test_accuracy,
    'KNN': knn_test_accuracy
}

best_method = max(accuracies, key=accuracies.get)
print("Test Accuracies:", accuracies)
print("Best performing method:", best_method, "with accuracy:", accuracies[best_method])