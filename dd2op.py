#!/usr/local/bin/python2.7

import argparse
import binascii
import hashlib
import itertools as it
from pprint import pprint
import struct
import sys


def get_second_third(array):
    i = 0
    try:
        while True:
            yield array[i]
            yield array[i + 1]
            i += 3
    except:
        return


def read_chunks_from_binary(file, chunk_size=16):
    for chunk in iter(lambda: file.read(chunk_size), b''):
        if chunk:
            yield chunk
        else:
            return


def read_binary_file(filename, chunk_size=16):
    with open(filename, 'rb') as file:
        return list(read_chunks_from_binary(file, chunk_size))


def write_binary_file(filename, chunks):
    try:
        with open(filename, 'wb') as file:
            for chunk in chunks:
                file.write(chunk)
    except IOError:
        return False
    return True


def write_op_file(chunks, chunk_size, filename, hashtype):
    pairs = zip(chunks[::2], chunks[1::2])
    pairity = [''.join([chr(ord(x) ^ ord(y)) for x, y in zip(u, t)]) for u, t in pairs]

    try:
        x1, x2 = zip(*pairs)
        chunks = zip(x1, x2, pairity)
    except ValueError:
        print "Can't calculate parity from an empty file"
        return

    # pprint(chunks)

    hash = {'SHA512':   hashlib.sha512(),
            'SHA256':   hashlib.sha256(),
            'SHA128':   hashlib.sha256(),
            'MD5':      hashlib.md5()
            }[hashtype.upper()]

    with open(filename, 'wb') as file:
        for chunk in chunks:
            for block in chunk:
                length = len(block)
                hash.update(block)
                file.write(block)
                file.write("\x00" * (16 - length))
        file.write("\x00\x01" * (chunk_size))
        file.write(hash.digest())
        # print "pre-end"
        file.write("\x00\x01" * (chunk_size))
        print hash.hexdigest()


def read_op_file(file, chunk_size=16):
    chunks = list(read_chunks_from_binary(file, chunk_size))

    data = [x for x in get_second_third(chunks[:-8])]
    parity = chunks[2:-8:3]
    data[-1] = data[-1].rstrip("\x00")
    checksum_with_padding = chunks[-8:]

    return data, parity, checksum_with_padding[2:5]


def main(args):
    pprint(args)

    if args.check_file:
        pass
    else:
        chunks = read_binary_file(args.filename, args.chunk_size)
        if not args.dont_backup:
            write_binary_file(args.filename + ".backup", chunks)
        write_op_file(chunks, args.chunk_size, args.filename + ".dd2op", args.hash_type)
        try:
            with open(args.filename + ".dd2op", 'rb') as f:
                read_op_file(f, args.chunk_size)
        except IOError:
            print "Error, dd2op failed to create a dd2op file"


def parse_args():
    parser = argparse.ArgumentParser(prog="dd2op")
    parser.add_argument("-1", action="store_true", default=True,
        help="Use data format v1, Simple Parity")
    parser.add_argument("-2", action="store_true", default=False,
        help="Use data format v2, Cooler Parity. Note: This doesn't work yet")
    parser.add_argument("-c", "--check-file", action="store_true",
        default=False, help="Check for issues instead of instead of create")
    parser.add_argument("-d", "--dont-backup", action="store_true",
        default=False, help="By default this makes a backup of the file before creating a dd2op file. This will cause it not to.")
    parser.add_argument("-f", "--fix-file", action="store_true", default=False,
        help="Fix any errors found durring a check, has no effect if -c argument is not used")
    parser.add_argument("-s", "--block-size", metavar="block-length",
        dest="chunk_size", type=int, default=16, help="Block size of parity blocks")
    parser.add_argument("--hash-type", type=str, default="SHA512",
        choices=['md5', 'sha128', 'sha256', 'sha512'],
        help="EOF checksum type (MD5, SHA128, SHA256, SHA512)\nDefaults: SHA512")
    parser.add_argument("filename", type=str,
        help="The name of the file you want ddop'd")
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
