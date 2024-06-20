import pandas as pd
import pandera as pa
from pandera.typing import Series, DataFrame

class MySchema(pa.SchemaModel):
    column1: Series[int] = pa.Field(le=10)
    column2: Series[float] = pa.Field(lt=-1.2)
    column3: Series[str] = pa.Field(str_startswith="value_")
    @pa.check("column3")
    def column_3_check(cls, series: Series[str]) -> Series[bool]:
        """Check that column3 values have two elements after being split with '_'"""
        return series.str.split("_", expand=True).shape[1] == 2

class MySchema2(pa.SchemaModel):
    column1: Series[int] = pa.Field(le=10)
    column2: Series[float] = pa.Field(lt=-1.2)
    column3: Series[str] = pa.Field(str_startswith="value_")
    @pa.check("column3")
    def column_3_check(cls, series: Series[str]) -> Series[bool]:
        """Check that column3 values have two elements after being split with '_'"""
        return series.str.split("_", expand=True).shape[1] == 2


# スキーマ定義 ※あんまり実用的ではない
# schema = pa.DataFrameSchema({
#     "column1": pa.Column(int, checks=pa.Check.le(10)),
#     "column2": pa.Column(float, checks=pa.Check.lt(-1.2)),
#     "column3": pa.Column(str, checks=[
#         pa.Check.str_startswith("value_"),
#         # series の入力を受け取り boolean か boolean 型の series を返すカスタムチェックメソッドを定義
#         pa.Check(lambda s: s.str.split("_", expand=True).shape[1] == 2)
#     ]),
# })

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


