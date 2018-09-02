import boto3
import json
import os
import pandas as pd
from botocore.exceptions import ClientError
from urllib.request import urlopen


def simple_function(url, sheet_name):
    file_name = url.split('/')[-1]
    print('file_name', file_name)
    with urlopen(url) as response, open(file_name, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    df = pd.read_excel(file_name, sheet_name=sheet_name)
    df.fillna('', inplace=True)
    data = list(df.T.to_dict().values())
    json_data = json.dumps(data)
    try:
        os.remove(file_name)
        print('removed file {}'.format(file_name))
    except OSError:
        pass
    try:
        s3 = boto3.resource('s3')
        s3.Bucket(S3_BUCKET_NAME).put_object(Key='data.json', Body=json_data)
        return True
    except ClientError as e:
        print(e)
        return False


simple_function(url=FILE_URL, sheet_name=SHEET_NAME)

