import zlib
import base64


def compress_text(text:str):
    compressed_data = zlib.compress(text.encode('utf-8'))
    return base64.b64encode(compressed_data).decode('utf-8')

def decompress_text(compressed_text:str):
    compressed_data = base64.b64decode(compressed_text.encode('utf-8'))
    return zlib.decompress(compressed_data).decode('utf-8')
