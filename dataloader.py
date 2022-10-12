import boto3 

# add the access key and the secret access key before starting
access_key = ''
secret_access_key = ''
bucket_name = 'sample-datasets-galaxeye'
bucket_read_path = 'rak_cicd_test/Read/'
bucket_write_path = 'rak_cicd_test/Write/'

client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key=secret_access_key)

def upload(file):
    client.upload_file(file, bucket_name, bucket_write_path+'UpdatedDatabase.csv') 

def update(file):
    client.upload_file(file, bucket_name, bucket_read_path+'Database.csv')

def download(file):
    client.download_file(bucket_name, bucket_read_path+'Database.csv', file)

if __name__ == "__main__":
    update('Data/Read/Database.csv')
    download('Data/Read/Database.csv')
    upload('Data/Write/Result.csv')
