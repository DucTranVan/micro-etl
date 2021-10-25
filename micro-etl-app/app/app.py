#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import logging
import pandas as pd
import os
import boto3
from botocore.exceptions import ClientError
from pydomo import Domo

# Environment variables
URL = os.environ['Url']
S3_BUCKET = os.environ['S3Bucket']
LOG_LEVEL = os.environ['LogLevel']
DOMO_ID = os.environ['DomoClientId']
DOMO_SECRET = os.environ['DomoSecret']
# Log settings
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
# domo client connect
domo_client = Domo(DOMO_ID, DOMO_SECRET, api_host='api.domo.com')

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# Lambda function handler
def lambda_handler(event, context):
    logger.info('######################### EVENT #####################')
    logger.info(event)
    
    df = pd.read_csv('weather.csv')
    dataset_id = domo_client.ds_create(df,"micro_etl_app_weather_new", "for testing domo")
    logger.info('## NUMBER OF ELEMENTS')
    logger.info(df.size)

    # Save files into S3
    upload_file("weather.csv", S3_BUCKET)

