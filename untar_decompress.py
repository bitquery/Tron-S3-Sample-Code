import lz4.frame
import tarfile
import boto3
import io

s3 = boto3.client('s3', aws_access_key_id='idd', aws_secret_access_key='keyy', region_name='us-east-1')
bucket_name = 'streaming-tron'
block_object_key = 'tron.blocks.s3/000054886000/000054886487_0000000003458057278ecebe85b54d89e4795f4c07efcefacadb7020f45babb2_71992297fe129c7f4b7d2212504a78cac21aea1ea58311211add19a835090762.block.tar.lz4'

blocks_local_path = 'C:Your Path/s3downloadblocks.tar.lz4'



# Attempt to download the file
s3.download_file(bucket_name, block_object_key, blocks_local_path)

# Read the compressed data from the file.
compressed_data = open(blocks_local_path, "rb").read()

# Decompress the data.
decompressed_data = lz4.frame.decompress(compressed_data)

# Wrap the decompressed data in a file object.
decompressed_file = io.BytesIO(decompressed_data)

# Extract the contents of the tar archive.
decompressed_file = tarfile.TarFile(fileobj=decompressed_file)
decompressed_file.extractall()