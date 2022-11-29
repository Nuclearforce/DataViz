import pandas as pd
import dask.dataframe as dd
ddf = dd.read_csv('../data/crypto_dataset/crypto-markets.csv', assume_missing=True)
ddf.to_parquet('../data/crypto_dataset/crypto-markets.parquet')