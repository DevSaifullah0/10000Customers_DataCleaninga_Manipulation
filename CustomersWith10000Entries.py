import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import re
df=pd.read_excel("C:/Users/ce/Desktop/python/PandasPython/customer_data_with_issues.xlsx")
print(df)
print(df.isnull().sum())
df.drop(columns=["Notes"],inplace=True)

df["Email"]=df["Email"].fillna(
df["Name"].str.lower().str.strip()+
"@example.org"
)
df["Email"]=df["Email"].str.lower().str.strip()
df["Address"]=df["Address"].fillna("Not Provided")
def normalize_phone(num):
    if pd.isna(num):
        return num
    # Convert to string and strip spaces
    num = str(num).strip()
    # Keep only digits
    digits = re.sub(r'\D', '', num)
    # Remove duplicate +1 or 001 at the start
    if digits.startswith('11'):  # e.g., +1+1
        digits = digits[1:]
    if digits.startswith('001'):
        digits = digits[3:]
    if digits.startswith('1') and len(digits) > 10:
        digits = digits[1:]
    # Keep only the first 10 digits (main number)
    main_number = digits[:10]
    return "+1" + main_number if main_number else None

# Apply normalization
df['Phone'] = df['Phone'].apply(normalize_phone)
df["Phone"]=df["Phone"].fillna(method="bfill",limit=2)
Mean=df["Zip"].mean(skipna=True)
df["Zip"]=df["Zip"].fillna(Mean)
df["Zip"]=df["Zip"].astype(int)
Filling_Col=["City","State","Last_Purchase","Membership_Level","Is_Active"]
for col in Filling_Col:
    df[col]=df[col].fillna(method="bfill",limit=3)
df["Birth_Date"] = df["Birth_Date"].fillna("Unknown")
if "Birth_Date" in df.columns:
    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    start = datetime(2018, 1, 1)
    end = datetime(2023, 12, 31)

    df["Birth_Date"] = df["Birth_Date"].astype(str)
    df["Birth_Date"] = df["Birth_Date"].apply(
        lambda x: random_date(start, end) if "unknown" in x.lower() else pd.to_datetime(x, errors="coerce")
    )
df.to_excel("10000Customer_Details.xlsx",index=False)
df.drop_duplicates()
df.reset_index(drop=True,inplace=True)
print(df.isnull().sum())
print(df.head(5))
print(df.dtypes)
