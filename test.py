from pathlib import Path
import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier

def main():
    model_path = Path("data/model.pkl")
    test_input_path = Path("data/test_input_data.csv")
    test_target_path = Path("data/test_target_data.csv")

    test_data = pd.read_csv(test_input_path)
    test_targets = pd.read_csv(test_target_path)

    # load pickled model
    with open(model_path, "rb") as f:
        # load and typehint the classifier
        clf: RandomForestClassifier = pickle.load(f)

    score = clf.score(test_data, test_targets["final_class"])

    print(f"Feature importances are: {clf.feature_importances_}\n")
    print(f"Accuracy is: {score}\n")
    print(f"True labels are: {test_targets}")
    print(f"Predicted labels are: {clf.predict(test_data)}")

if __name__=="__main__":
    main()