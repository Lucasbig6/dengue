import pandas as pd
import polars as pl

try:
    df = pl.read_parquet("ingestion/dengue.parquet", n_rows=10)
    print("Columns:", df.columns)
    print("\nSample Data:\n", df.head())
    
    # Check for Piauí indicators
    # Typically Sinam uses 'ID_AGRAVO' for disease, 'SG_UF' for state, 'ID_MUNICIP' for city code
    # Let's check if 'SG_UF' exists and 'ID_MUNICIP'
    cols = df.columns
    if 'SG_UF' in cols:
        print("\nUnique UFs in sample:", df['SG_UF'].unique().to_list())
    
    # Get all column names to check for SINAM fields
    df_full_schema = pl.read_parquet("ingestion/dengue.parquet", n_rows=1)
    print("\nFull Schema:", df_full_schema.columns)

except Exception as e:
    print(f"Error: {e}")
