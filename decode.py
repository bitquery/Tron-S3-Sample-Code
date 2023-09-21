import block_message_pb2
import base64
import binascii


with open("block_proto_message", "rb") as f:
    message_data = f.read()

block_message = block_message_pb2.BlockHeader()
block_message.ParseFromString(message_data)

decoded_hash = base64.b64decode(block_message.Hash)
hex_hash = binascii.hexlify(decoded_hash)
print(hex_hash)



