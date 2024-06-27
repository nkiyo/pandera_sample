import sys
import numpy as np
import pandas as pd
import pandera as pa
from jsonschema import validate
from pandera.typing import DataFrame
from schema import MySchema, MySchema2,MySchema3, validate_3_or_4
import yaml
import json

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

with open("config_schema.json", 'r') as file:
    config_schema = json.load(file)

validate(config, config_schema)

# TODO NGデータがあるとき、Falseを返す
# TODO NGデータを取り除いたdfを返す

def create_dataframe() -> DataFrame[MySchema] | None:
    # バリデーション用のデータ
    df = pd.DataFrame({
        "column1": [1, 4, 0, 10, 9],
        "ほげ": [1, 4, 0, 10, 9],
        "column2": [-1.3, None, -2.9, -10.1, -20.4],
        "column3": ["value_あ", "value_ab", "value_中原", "value_2", "value_1"],
    })
    try:
        validated_df = MySchema.validate(df)
    except pa.errors.SchemaError as e:
        print("validate error")
        return None
    # print("validat succeeded")
    return validated_df


def convert_dataframe(df: DataFrame[MySchema]) -> DataFrame[MySchema2]:
    # TODO 複雑な変換処理
    return MySchema2.validate(df)

mydf: DataFrame[MySchema] | None = create_dataframe()
if mydf is None:
    sys.exit(1)
# print(mydf)
mydf2: DataFrame[MySchema2] = convert_dataframe(mydf)
# print(mydf2)


df3 = pd.DataFrame({
    "PassengerId": [1, 2, 3, 4],
    "Survived": [1, None, 0, 1],
    "hoge": [1, None, 0, 1],
})
df4 = pd.DataFrame({
    "PassengerId": [1, 2, 3, 4],
    "Survived": [1, 0, 0, 1],
    "hoge": [1, None, 0, 1],
})
# validated_df3 = MySchema3.validate(df3)
# validated_df3 = MySchema3.validate(df3)
validated_df3 = validate_3_or_4(df3)
validated_df4 = validate_3_or_4(df4)

print(validated_df3)
print(validated_df4)
