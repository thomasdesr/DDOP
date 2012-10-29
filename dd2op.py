#!/usr/local/bin/python2.7

import hashlib
from pprint import pprint
import struct
import sys

#0:md5:16
#1:md5:16
#2:sha256:32
#3:sha512:64
#4:sha3

def build_header():
    bin_length = 512
    total_len = 1024
    block_len = 128
    block_hash_type = 0
    final_hash_type = 3
    encrypted = 0
    
    padding = 494
    header = struct.pack("iiihhh{padding}s".format(padding=padding), bin_length, total_len, block_len, block_hash_type, final_hash_type, encrypted, '\xFF' * padding)
    return header

def read_header(file):
    try:
        header = file.read(512)
    except IOError:
        print "Unable to read the header, corruption suspected."
    
    return struct.unpack("iiihhh494s", header)
    

def read_chunks_from_binary(file, chunk_size=1024*64):
    for chunk in iter(lambda: file.read(chunk_size), b''):
        if chunk:
            yield chunk
        else:
            return

def read_chunks_from_opdd(file, chunk_size=1024*64, hash_type=0):
    while True:
        try:
            chunk = file.read(chunk_size)
            hash = file.read(64)
            if hash_type == 0:
                if '\x00' * 64 == hash:
                    yield chunk
            elif hash_type == 1:
                if hashlib.md5(chunk).digest() + '\x00' * 48:
                    yield chunk
            elif hash_type == 2:
                if hashlib.sha256(chunk).digest() + '\x00' * 32:
                    yield chunk
            elif hash_type == 3:
                if hashlib.sha512(chunk).digest():
                    yield chunk
            else:
                yield None
        except IOError:
            return


def hash_chunks(chunks, hash_type):
    for chunk in chunks:
        yield chunk
        if hash_type == 0:
            yield '\x00' * 64
        elif hash_type == 1:
            yield hashlib.md5(chunk).digest() + '\x00' * 48
        elif hash_type == 2:
            yield hashlib.sha256(chunk).digest() + '\x00' * 32
        elif hash_type == 3:
            yield hashlib.sha512(chunk).digest()

def read_op_file(header_length, file):
    header = struct.unpack("iiihhh494s", file.read(512))
    
    chunks = list(read_chunks_from_opdd(file, 256, 1))
    
    return chunks

def read_binary_file(file):
    bin = list(read_chunks_from_binary(file, 256))
    # pprint([type(x) for x in bin])
    # pprint([len(x) for x in bin])
    # pprint(bin)
    return bin

def write_op_file(header, chunks, file):
    file.write(header)
    
    chunks = list(hash_chunks(chunks, 1))
    pprint(len(chunks))
    
    for chunk in chunks:
        file.write(chunk)

def main():
    with open(sys.argv[1], 'rb') as f:
        chunks = read_binary_file(f)
    with open(sys.argv[2], 'wb') as f:
        header = build_header()
        pprint(header[:18])
        write_op_file(header, chunks, f)
    with open(sys.argv[2], 'rb') as f:
        pprint(read_header(f)[:-1])
    
    # with open(sys.argv[2], 'rb') as f:
        # pprint(read_op_file(512, f))
    
    
if __name__ == "__main__":
    main()