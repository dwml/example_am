from pathlib import Path
import pandas as pd

from data_validation.objects import SubjectSchema

def main():
    database_path = Path("data/Database TraumaTIPS Follow-up study 24102024.sav")
    validated_path = Path("data/database_validated.csv")

    df = pd.read_spss(database_path)

    # Due to time constraints I just drop na for now
    df.dropna(inplace=True)

    
    df_valid = SubjectSchema(df)

    df_valid.to_csv(validated_path)


    


if __name__ == "__main__":
    main()
