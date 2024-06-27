import pandera as pa
from pandera.typing import Series, DataFrame
from typing import Optional

class MySchema(pa.SchemaModel):
    column1: Series[int] = pa.Field(le=10)
    ほげ: Series[int] = pa.Field(le=10)
    column2: Series[float] = pa.Field(lt=-1.2, nullable=True)
    column3: Series[str] = pa.Field(str_startswith="value_", str_length={"min_value": 7, "max_value":8})
    @pa.check("column3")
    def column_3_check(cls, series: Series[str]) -> Series[bool]:
        """Check that column3 values have two elements after being split with '_'"""
        return series.str.split("_", expand=True).shape[1] == 2

class MySchema2(pa.SchemaModel):
    column1: Series[int] = pa.Field(le=10)
    column2: Series[float] = pa.Field(lt=-1.2, nullable=True)
    column3: Series[str] = pa.Field(str_startswith="value_")
    @pa.check("column3")
    def column_3_check(cls, series: Series[str]) -> Series[bool]:
        """Check that column3 values have two elements after being split with '_'"""
        return series.str.split("_", expand=True).shape[1] == 2

# DataFrameのある列にintとNoneが混在してると、Pandasはその列をfloatとして扱う
# 欠点：この型を使うと、floatが混在することを許容してしまう
# 欠点：Noneが混在してないとき、Pandasはその列をintとして扱うためNGになる
int_or_none = float

# https://zenn.dev/anieca/articles/37157cf65d70ea
class MySchema3(pa.DataFrameModel):
    PassengerId: int = pa.Field(nullable=False, unique=True)
    Survived: int_or_none= pa.Field(nullable=True, isin=(0,1))
    # Survived: Series[int_or_none]= pa.Field(nullable=True, in_range={"min_value": 0, "max_value": 1})
    # Cabin: Series[str] = pa.Field(nullable=True)
    # Pclass: Series[int] = pa.Field(nullable=False, isin=(1, 2, 3))
    # Sex: Series[str] = pa.Field(nullable=False, isin=("male", "female"))
    # Age: Series[float] = pa.Field(nullable=True, in_range={"min_value": 0, "max_value": 100})
    # Embarked: Series[str] = pa.Field(nullable=True, str_length=1, isin=("S", "C", "Q"))
    
    # https://pandera.readthedocs.io/en/stable/reference/generated/pandera.api.pandas.model_config.BaseConfig.html#pandera-api-pandas-model-config-baseconfig
    class Config:
        # 余分な列があったらNGにする
        # strict = True
        # 余分な列があったら削除する
        strict = "filter"

class MySchema4(pa.DataFrameModel):
    PassengerId: int = pa.Field(nullable=False, unique=True)
    Survived: int = pa.Field(nullable=True, isin=(0,1))
    class Config:
        strict = "filter"

@pa.check_types
def validate_3_or_4(df: DataFrame[MySchema3] | DataFrame[MySchema4]) -> DataFrame[MySchema3] | DataFrame[MySchema4]:
    return df

