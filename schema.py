import pandera as pa
from pandera.typing import Series, DataFrame

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
