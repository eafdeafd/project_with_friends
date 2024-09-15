import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import threading
import sys

class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()

class S3Client():
    def __init__(self):
        self.s3 = boto3.client('s3')

    def list_s3(self):
        '''
        Prints available buckets
        '''
        response = self.s3.list_buckets()
        print('Existing buckets:')
        for bucket in response['Buckets']:
            print(f'  {bucket["Name"]}')
    
    def upload_file(self, file_name, bucket='our-vct-bucket', object_name=None):
        """Upload` a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            '''
            Optionally, use callback such as ProgressPercentage to track upload progress per file
            And ExtraArgs for additional usage i.e. ExtraArgs={'Metadata': {'mykey': 'myvalue'}}
            s3.upload_file(
                'FILE_NAME', 'BUCKET_NAME', 'OBJECT_NAME',
                Callback=ProgressPercentage('FILE_NAME')
            )
            '''
            response = self.s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def download(self, file_name, bucket='our-vct-bucket', object_name=None):
        '''
        """Download` a file from the s3 bucket

        :param file_name: Filename to download to
        :param bucket: Bucket to download from
        :param object_name: S3 object to download
        :return: True if file was downloaded, else False
        '''
        if object_name is None:
            logging.warning('S3 download with no target')
            return False
        try:
            # same optional params as upload
            self.s3.download_file(bucket, object_name, file_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    

if __name__ == "__main__":
    load_dotenv()
    # example uploading and downloading files from s3
    client = S3Client()
    client.upload_file('temp/test.txt', object_name='test2.txt')
    client.download('temp/test3.txt', object_name='test2.txt')