import boto3

# Initialize the S3 client
s3_client = boto3.client('s3')

# Common Crawl S3 bucket
bucket = 'commoncrawl'

# List files in the crawl-data directory
def list_files_in_crawl_data():
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix='crawl-data/', Delimiter='/')
    if 'CommonPrefixes' in response:
        for prefix in response['CommonPrefixes']:
            print(f"Subdirectory: {prefix['Prefix']}")
            # List the files under this prefix
            list_files_under_prefix(prefix['Prefix'])
    else:
        print("No subdirectories found under 'crawl-data/'.")

# List files under a specific prefix
def list_files_under_prefix(prefix):
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"File: {obj['Key']}")
    else:
        print(f"No files found in {prefix}.")

# Run the function to list files under 'crawl-data/'
list_files_in_crawl_data()
