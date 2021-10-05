from flask import Flask, render_template, Response, send_file
import boto3
import pandas as pd
import io
import json
import zipfile
import configparser
import os

#If you have your own aws cli set up, comment these lines
config = configparser.ConfigParser()
config.read('aws.config')

session = boto3.Session(
    aws_access_key_id=config.get('aws_cred', 'secret_key'),
    aws_secret_access_key=config.get('aws_cred', 'secret_value'),
)

s3_resource = session.resource('s3')
s3_client = session.client('s3')

#If you have your own aws cli set up, uncomment this
# s3_resource = boto3.resource('s3')
# s3_client = boto3.client('s3')


BUCKET = 'ceres-technical-challenge'
HOMEPAGE = 'Homepage.html'

app = Flask(__name__)

file_metadata = {}
filenames = []


@app.route('/')
def hello_world():
   return render_template(HOMEPAGE)

@app.route('/images')
def get_images():
    if not filenames:
        get_filenames()
    return render_template(HOMEPAGE, result = filenames)

@app.route('/download/<file_name>')
def download_image(file_name):
    local_file = s3_client.get_object(Bucket=BUCKET, Key=file_name)

    return Response(
        local_file['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename="+file_name}
    )

@app.route('/refresh')
def refresh_page():
    filenames = []
    file_metadata = {}
    return render_template(HOMEPAGE)

@app.route('/downloadall')
def download_all():
    with zipfile.ZipFile("AllFiles.zip", "a") as zip_file:
        for file in filenames:
            local_file = s3_client.get_object(Bucket=BUCKET, Key=file)
            zip_file.writestr(file, local_file['Body'].read())
    
    
    return send_file('AllFiles.zip',
            mimetype = 'zip',
            attachment_filename= 'AllFiles.zip',
            as_attachment = True)

@app.route('/metadata/<file_name>')
def get_metadata(file_name):

    if file_name in file_metadata:
        return render_template(HOMEPAGE, metadata = file_metadata[file_name], result = filenames)
    
    metadata = s3_client.get_object(Bucket=BUCKET, Key='metadata.txt')

    df = pd.read_csv(io.BytesIO(metadata['Body'].read()), sep='\t')

    columns = list(df)

    for row in df.itertuples(index=False):
        values = {}
        for i in range(1, len(df.columns)):
            values[columns[i]] = row[i]
        file_metadata[row[0]] = values

    return render_template(HOMEPAGE, metadata = file_metadata[file_name], result = filenames)


def get_filenames():
    my_bucket = s3_resource.Bucket(BUCKET)
    for file_obj in my_bucket.objects.all():
        filenames.append(file_obj.key)


if __name__ == '__main__':
   app.run()