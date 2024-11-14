import boto3
import os
import pandas as pd
import gzip
import io
from warcio.archiveiterator import ArchiveIterator

# Initialize the S3 client (uses your AWS CLI configuration by default)
s3_client = boto3.client('s3')

# URLs you want to filter
urls_to_search = ['https://www.reddit.com/r/travel/', 
                  'https://www.cntraveler.com/', 
                  'https://www.lonelyplanet.com/', 
                  'https://www.nationalgeographic.com/travel', 
                  'https://www.travelandleisure.com/', 
                  'https://www.tripadvisor.com/', 
                  'https://www.foodandwine.com/travel/', 
                  'https://www.fodors.com/', 
                  'https://www.roughguides.com/', 
                  'https://www.tasteatlas.com/']

# Function to save content to a file
def save_document(url, content):
    folder_path = os.path.join("output")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"document_{hash(content)}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Document saved for URL {url} at {file_path}")

def download_common_crawl_warc_files(prefix):
    # Common Crawl S3 bucket
    bucket = 'commoncrawl'
    
    # List files in the specified S3 prefix (can be a date or specific category)
    print(f"Listing objects in S3 bucket with prefix {prefix}...")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    
    if 'Contents' not in response:
        print(f"No files found in prefix {prefix}.")
        return
    
    # Iterate through the files
    for obj in response['Contents']:
        file_key = obj['Key']
        
        # Only process WARC files
        if file_key.endswith(".warc.gz"):
            print(f"Downloading {file_key}...")
            
            # Get the object from S3
            obj_data = s3_client.get_object(Bucket=bucket, Key=file_key)
            
            # If it's a gzip file, decompress it
            with gzip.GzipFile(fileobj=io.BytesIO(obj_data['Body'].read())) as f:
                # Read the WARC file using warcio
                for record in ArchiveIterator(f):
                    if record.rec_type == 'response':  # Ensure it's an HTTP response record
                        url = record.rec_headers.get_header('WARC-Target-URI')
                        print(f"Found URL: {url}")
                        if any(url.startswith(u) for u in urls_to_search):  # Check if the URL matches
                            try:
                                content = record.payload.read().decode('utf-8', 'ignore')
                                print(f"URL matched: {url}. Saving document...")
                                save_document(url, content)
                                
                                # Optionally, store the data in a CSV (if needed)
                                pd.DataFrame([{'url': url, 'content': content}]).to_csv(f"{url.replace('/', '_')}.csv", index=False)
                            except Exception as e:
                                print(f"Error processing content for URL {url}: {e}")
        else:
            print(f"Skipping non-WARC file: {file_key}")

# Example URL prefixes for Common Crawl (this could be more specific to the type of data you're looking for)
urls = ['crawl-data/CC-MAIN-2023-50/']  # Specify the Common Crawl prefix (you can adjust this to a more specific dataset)
for url in urls:
    download_common_crawl_warc_files(url)
