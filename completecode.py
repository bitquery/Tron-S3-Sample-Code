import boto3
from botocore.exceptions import ClientError
import lz4.frame
import json
import binascii
import block_message_pb2
from google.protobuf.json_format import MessageToJson
import logging
import base64


logging.basicConfig(level=logging.INFO)

s3 = boto3.client('s3', aws_access_key_id='your id', aws_secret_access_key='jj', region_name='us-east-1')
bucket_name = 'streaming-tron'
block_object_key = 'tron.blocks.s3/000054661000/000054661618_00000000034211f2726c91979ad98fcd9510494bd55f2019b5534e95091ef39b_28c9404c29e19b3236da111504443b110078ea78a0ef8818b9812bf0b5232ca3.block.tar.lz4'

blocks_local_path = 'C:/Your Path/s3downloadblocks.lz4'

import re

binary_data_regex = re.compile(rb'[\x00-\x08\x10-\x1f\x7f-\xff]')

def remove_binary_data(decompressed_data):
  """Removes binary data from the given string.

  Args:
    decompressed_data: A string containing decompressed data.

  Returns:
    A string containing the decompressed data with the binary data removed.
  """

  decompressed_data = binary_data_regex.sub(b'', decompressed_data)
  return decompressed_data.decode()


try:
    # Attempt to download the file
    s3.download_file(bucket_name, block_object_key, blocks_local_path)

    # Step 1: Decompress the LZ4 data
    with open(blocks_local_path, 'rb') as lz4_file:
        # Decompress the file in chunks
        decompressed_data = b''
        for chunk in iter(lambda: lz4_file.read(1024 * 1024), b''):
            decompressed_data += lz4.frame.decompress(chunk)
                 
    
    decompressed_data = remove_binary_data(decompressed_data)
    # print(decompressed_data)
  
    # Write the JSON data to a file
    output_file_path = 'output.json'
    # block_headers = block_message_pb2.BlockHeader()

    # block_headers.ParseFromString(bytes(decompressed_data,'utf-8'))
    with open(output_file_path, 'w') as json_file:
        json.dump(decompressed_data, json_file, indent=4, sort_keys=True)

    print(f"JSON data has been written to {output_file_path}")

except ClientError as e:
    # Handle other error codes as well
    if e.response['Error']['Code'] in ['404', '500', '503']:
        logging.error(e)
    else:
        logging.exception(e)
