import pandas as pd 

df=pd.read_parquet("./data/postgres/2024-01-01/orders/20240206_030020-898970.parquet",engine='pyarrow')
print(df.dtypes)
