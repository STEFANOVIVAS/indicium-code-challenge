import pandas as pd 

df=pd.read_parquet("./data/postgres/2024-01-01/ecommerce/public-products/20240205_234115-512868.snappy.parquet",engine='pyarrow')
print(df['unit_price'])
