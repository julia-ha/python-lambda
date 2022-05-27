import sys

import os
import logging

import ocrmypdf

import boto3
import botocore

from flask import Flask, request, make_response
from flask_cors import CORS

import requests
logging.getLogger('requests').setLevel(logging.WARNING)

log = logging.getLogger('ocrmypdf')
log.setLevel(logging.INFO)


def _pdf_get(event, context):
  object_key = "OBJECT_KEY"  # replace object key
  file_content = s3_client.get_object(
      Bucket=S3_BUCKET, Key=object_key)["Body"].read()
  print(file_content)


def reocr_pdf(infile, outfile, **kwargs):
    ocrmypdf.ocr(infile, outfile, **kwargs)

def get_pdf_url(doi):
    return requests.get(f'https://b49tnk5c88.execute-api.us-east-1.amazonaws.com/prod/pdf-url/{doi}').text

def get_pdf(url, fname):
    resp = requests.get(url)
    with open(fname, 'wb') as fp:
        fp.write(resp.content)

def _s3_upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    """
    s3 = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    ).resource('s3')
    """

    s3 = boto3.resource('s3')
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    pdfFileObj = open(file_name, 'rb')

    object = s3.Object(bucket, object_name)
    return object.put(Body=pdfFileObj)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def _s3_get_file(bucket, object_name, file_name):
    """Download a file from an S3 bucket

    :param file_name: File name to put local download
    :param bucket: Bucket to download from
    :param object_name: S3 object name to download
    """
    """
    s3 = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    ).resource('s3')
    """
    s3 = boto3.resource('s3')

    s3_bucket = s3.Bucket(bucket)
    file_path = '/tmp/' + file_name
    s3_bucket.download_file(object_name, file_path)


def handler(event, context):

   # Downloading '652164.pdf' from s3 bucket 'ocr-pdfs' into local file 'download_652164.pdf'
   _s3_get_file('ocr-pdfs', '652164.pdf', 'download_652164.pdf')

   # Uploading local file 'test.pdf' into s3 bucket 'ocr-pdfs' to object name 'test.pdf'
   # _s3_upload_file('test.pdf', 'ocr-pdfs', 'test.pdf')

   return 'Hello from AWS Lambda using Python' + sys.version + '!'       