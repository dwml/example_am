from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

from data_validation.objects import SubjectSchema

def main():
    # Define paths
    database_path = Path("data/Database TraumaTIPS Follow-up study 24102024.sav")
    training_input_path = Path("data/training_input_data.csv")
    training_target_path = Path("data/training_target_data.csv")
    test_input_path = Path("data/test_input_data.csv")
    test_target_path = Path("data/test_target_data.csv")

    df = pd.read_spss(database_path)

    # Due to time constraints I just drop na for now
    df.dropna(inplace=True, subset=["amnesia", "impact.of.prior.traumatic.events"])

    df_validated = SubjectSchema(df)

    # Put target and input in separate dataframes
    target = df_validated["final_class"]
    input_data = df_validated.drop(columns=["id", "final_class"])

    # Since the outcome class is mostly zero I stratify and choose a larger test_size than default
    train_input, test_input, train_target, test_target = train_test_split(input_data, target, test_size=0.4, stratify=target)

    # Save
    train_input.to_csv(training_input_path, index=False)
    train_target.to_csv(training_target_path, index=False)
    test_input.to_csv(test_input_path, index=False)
    test_target.to_csv(test_target_path, index=False)


if __name__ == "__main__":
    main()
