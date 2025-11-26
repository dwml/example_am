from pathlib import Path
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pickle

def main():
    model_path = Path("data/model.pkl")
    training_input_path = Path("data/training_input_data.csv")
    training_target_path = Path("data/training_target_data.csv")

    training_data = pd.read_csv(training_input_path)
    training_targets = pd.read_csv(training_target_path)

    # define grid for grid search
    param_grid = {
        "n_estimators": [10, 100, 200, 300],
    }

    # instantiate grid search with random forest classifier
    rfc = RandomForestClassifier()
    clf = GridSearchCV(rfc, param_grid, cv=2) # least populated class has only 2 members
    clf.fit(training_data, training_targets["final_class"])

    # Save best model 
    best_model = clf.best_estimator_
    with open(model_path, "wb") as f:
        pickle.dump(best_model,f)


if __name__ == "__main__":
    main()
