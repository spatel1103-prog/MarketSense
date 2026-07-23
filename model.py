from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


def train_models(data):

    FUTURE_DAYS = 126

    # make a column that has the future days closing price using shift
    data["Future_Close"] = data["Close"].shift(-FUTURE_DAYS)

    # make a new column to create percentage return over 6 months
    data["Future_Return"] = (data["Future_Close"] - data["Close"]) / data["Close"]

    # we want to check if future return is at least 10%
    TARGET_RETURN = 0.10

    # create column named future_up that displays 1 if its future return is at least 10% and 0 otherwise
    data["Future_Up"] = (data["Future_Return"] >= TARGET_RETURN).astype(int)

    # remove rows with NaN
    clean_data = data.dropna()

    X = clean_data[[
        "Daily_Return", "MA_5_Distance",
        "MA_20_Distance", "Momentum_5",
        "Volatility_20", "Volume_Change", "RSI_14"
    ]]

    y = clean_data["Future_Up"]

    # train on 80% of the data and test on 20%
    # dont shuffle data because this data is chronological
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # create logistic regression model object
    model = LogisticRegression()

    # model looks at training examples and tries to learn patterns between X and y
    model.fit(X_train, y_train)

    # predictions is a NumPy array now not a dataframe
    predictions = model.predict(X_test)

    # calculates accuracy of model using its results and the real results
    accuracy = accuracy_score(y_test, predictions)

    # now use decision tree model to compare against logistics regression model
    # set random state to 42 so that it builds the random tree the same way every time u run
    tree_model = DecisionTreeClassifier(random_state=42)

    tree_model.fit(X_train, y_train)
    tree_predictions = tree_model.predict(X_test)
    tree_accuracy = accuracy_score(y_test, tree_predictions)

    # now use random forest to create a different model
    # random forest is usually better than decision tree b/c it builds many different trees on different samples of data
    # n_estimators=100 means have the model build 100 decision trees
    forest_model = RandomForestClassifier(n_estimators=100, random_state=42)

    forest_model.fit(X_train, y_train)
    forest_predictions = forest_model.predict(X_test)
    forest_accuracy = accuracy_score(y_test, forest_predictions)

    # see which model was the most accurate
    best_accuracy = accuracy
    best_prediction = predictions[-1]
    best_model_name = "Logistic Regression"

    if tree_accuracy > best_accuracy:
        best_accuracy = tree_accuracy
        best_prediction = tree_predictions[-1]
        best_model_name = "Decision Tree"

    if forest_accuracy > best_accuracy:
        best_accuracy = forest_accuracy
        best_prediction = forest_predictions[-1]
        best_model_name = "Random Forest"

    return {
        "X": X,
        "accuracy": accuracy,
        "tree_accuracy": tree_accuracy,
        "forest_accuracy": forest_accuracy,
        "best_accuracy": best_accuracy,
        "best_prediction": best_prediction,
        "best_model_name": best_model_name,
        "forest_model": forest_model,
    }