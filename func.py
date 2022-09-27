import pandas as pd 

def write_csv(df):
    num_values = len(df)
    df["Z"] = 0
    for i in range(num_values):
        df.loc[i,"Z"] = df.loc[i,"X"] + df.loc[i,"Y"]
    return df

if __name__ == "__main__":
    df = pd.read_csv('Data/Read/Database.csv')
    df = write_csv(df)
    df.to_csv('Data/Write/Result.csv', index=False)