import pandas as pd
from pysus.online_data.SINAN import download

print("Baixando dados de dengue...")

dataset = download("DENG", 2026)

df = dataset.to_dataframe()

print("Total registros:", len(df))
print(df.head())

df.to_parquet("dengue.parquet", index=False)