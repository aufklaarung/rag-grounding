from google.cloud import storage

storage_client = storage.Client()

def read_file_from_gcs(bucket, blob_name, mode="text") -> str | bytes:
    """
    Reads the content of a file from GCS in the specified mode.

    Args:
        bucket (google.cloud.storage.bucket.Bucket): GCS bucket object.
        blob_name (str): Path to the file in GCS.
        mode (str): One of "text" or "binary".

    Returns:
        str or bytes: File content.
    """
    blob = bucket.blob(blob_name)
    if mode == "binary":
        return blob.download_as_bytes()
    elif mode == "text":
        return blob.download_as_text(encoding="utf-8")
    else:
        raise ValueError(f"Unsupported mode: {mode}")