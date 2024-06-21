import pandas as pd
from jsonschema import validate
from pandera.typing import DataFrame
from schema import MySchema, MySchema2
import yaml
import json

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("config_schema.json", 'r') as file:
    config_schema = json.load(file)

validate(config, config_schema)



# NGデータがあると、ここで異常終了する 
# validated_df = schema(df)

# TODO NGデータがあるとき、Falseを返す
# TODO NGデータを取り除いたdfを返す
# print(validated_df)

def create_dataframe() -> DataFrame[MySchema]:
    # バリデーション用のデータ
    df = pd.DataFrame({
        "column1": [1, 4, 0, 10, 9],
        "column2": [-1.3, -1.4, -2.9, -10.1, -20.4],
        "column3": ["value_1", "value_2", "value_3", "value_2", "value_1"],
    })
    return MySchema.validate(df)

def convert_dataframe(df: DataFrame[MySchema]) -> DataFrame[MySchema2]:
    # TODO 複雑な変換処理
    return MySchema2.validate(df)

mydf: DataFrame[MySchema] = create_dataframe()
print(mydf)
mydf2: DataFrame[MySchema2] = convert_dataframe(mydf)
print(mydf2)


