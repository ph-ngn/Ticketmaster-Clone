import boto3


class S3BUCKET:
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key, region_name):
        self.bucket_name = bucket_name
        self.region_name = region_name
        self.client = boto3.client('s3',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=region_name)

    def upload_file(self, file, user):
            self.client.upload_fileobj(file,
                                    self.bucket_name,
                                    f'{user}/{file.filename}',
                                    ExtraArgs={
                                    "ContentType":  file.content_type})

            return self.get_file_url(file.filename, user)

    def get_file_url(self, file, user):
        return f'https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{user}/{file}'

    def upload_files(self, files, user):
        file_paths = []
        for file in files:
            file_paths.append(self.upload_file(file, user))

        return file_paths