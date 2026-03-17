import polars as pl
import pandas as pd

df = pl.read_parquet("ingestion/dengue.parquet")
df_pi = df.filter(pl.col("uf_residencia") == "22")

print(f"Total rows for PI: {len(df_pi)}")
print("\nUnique Sexo:", df_pi["sexo"].unique().to_list())
print("\nUnique Classificacao:", df_pi["classificacao_final"].unique().to_list())
print("\nUnique Evolucao:", df_pi["evolucao"].unique().to_list())
print("\nSample Municipios:", df_pi["municipio_residencia"].unique().head(10).to_list())
