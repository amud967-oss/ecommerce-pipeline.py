import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv() 

db_user = os.getenv("DB_USER")
db.password = os.getenv("DB_PASSWORD")
db.host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

engine = create_engine(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
#1. extract it
print("Reading CSV ...")
df = pd.read_csv("sales_data_sample.csv", encoding= 'latin1')
print(f"Before cleaning: {len(df)} rows")

# 2. Transform it 
df.columns = df.columns.str.lower().str.replace(" ", "_")

#drop rows


#Remove duplicates
df = df.drop_duplicates()

#Fix date
df['orderdate'] = pd.to_datetime(df['orderdate'], errors='coerce')
df = df.dropna(subset=['orderdate'])


# Remove cancelled
df = df[df['status'] != 'Cancelled']
df = df[df['sales'] > 0]

print(f"After cleaning: {len(df)} rows")

#Load it into postgres
print("Loading to Postgres...")
engine = create_engine("postgresql://postgres:Dave/234@localhost/postgres")
df.to_sql("ecommerce_sales", engine, if_exists="replace", index=False)
print("Loaded! Done!")