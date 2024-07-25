from google.cloud import storage
import os

class CloudStorage:

    def __init__(self, project_id: str, bucket_name: str):
        self.client = storage.Client(project=project_id)
        self.bucket_name = bucket_name

    def upload_files(
        self,
        source_dir: str
    ):
        """
        Uploads all files within the specified directory to the GCS bucket.
        
        :param source_directory: Path to the directory containing files to upload.
        :param destination_blob_prefix: Prefix for the destination blobs in the bucket.
        """
        bucket = self.client.bucket(self.bucket_name)

        for root, _, files in os.walk(source_dir):
            for file in files:
                source_file_path = os.path.join(root, file)
                blob = bucket.blob(file)
                blob.upload_from_filename(source_file_path)
                print(f"Uploaded {source_file_path} to {file}")
