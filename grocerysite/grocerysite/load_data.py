from grocerysite import models # import specific models from grocerysite
import sys
import pandas as pd # for reading csv files

def load_model(model_name, file_name):
    data = pd.read_csv(file_name)
    DataModel = getattr(models, model_name)

    for idx, row in data.iterrows():
        record = DataModel()
        for field in row.index:
            print(f"{field}:{row[field]}")
            setattr(record, field, row[field])
    
        record.save()

if __name__ == "__main__":
    model_name = sys.argv[1]
    file_name = sys.argv[2]
    load_model(model_name, file_name)

