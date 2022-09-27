import pandas as pd
from func import write_csv
from fastapi import FastAPI
from pydantic import BaseModel
from dataloader import upload, download, update

'Folder locations in the local'
database = 'Data/Read/Database.csv'
updated_database = 'Data/Write/UpdatedDatabase.csv'

'Download the data from S3'
download(database)

app = FastAPI()

class Item(BaseModel):
    X: int
    Y: int

@app.get('/app/welcome')
def welcome():
    return 'Welcome to my app'

'update the values in the databse by posting requests'
@app.post('/app/data')
def get_data(data: Item):
    x = data.X
    y = data.Y
    df = pd.read_csv(database) # Read from downloaded database
    new_index = len(df)
    df.loc[new_index, 'X'] = x
    df.loc[new_index, 'Y'] = y
    df.to_csv(database, index=False) # Update the local database
    update(database) # Update the S3 database
    df = write_csv(df) # calulate the updated database
    df.to_csv(updated_database, index=False) # Update the local updated database
    upload(updated_database) # Update the S3 updated database
    return 'data_received_successdully'