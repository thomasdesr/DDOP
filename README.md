DDOP
====

dd2op, because dd is way too OP'd as a forensics format. It \
however, like every other format has has a problem. That being \
that in cases of bit flips in the storage or transmission medium \
that whole chunk of data is lost.



Data Format v1:
 +-----------------------------------------------------------------------------+
 ¦ Data Block ¦ Parity ¦ Data Block ¦ Parity ¦ [Repeat] ¦ Final Checksum Block ¦
 +-----------------------------------------------------------------------------+

 While this format can allow for the recovery of data, it has no \
 ability to detect if there has been corruption of the parity values\
 which could allow for additional corruption of data. Although \
 as long as the final checksum block remains unaffected, it is \
 possible for recovery to occur by brute forcing flipped bits and \
 by treating all three bits as malformed data. This is however not \
 how parity is supposed to work and is really a workaround until \
 Data Format v2 can be fully implemented.


Dava Format v2:
 +-------------------------+
 ¦ Data Block ¦ Parity bit ¦
 +-------------------------+
 ¦ Data Block ¦ Parity bit ¦
 +-------------------------+
 ¦        [Repeat]         ¦
 +-------------------------+
 ¦  Vertical Parity Values ¦
 +-------------------------+
 ¦   Final Checksum Block  ¦
 +-------------------------+

 Data Format v2 is where this actually really turns into a parity \
 data recovery format. With the additoin of the horizontal and \
 vertical parity it makes it truely able to recover data with a \
 reasonable degree of certainty.

usage: dd2op [-h] [-1] [-2] [-c] [-d] [-f] [-s block-length]
             [--hash-type {md5,sha128,sha256,sha512}]
             filename

positional arguments:
  filename              The name of the file you want ddop'd

optional arguments:
  -h, --help            show this help message and exit
  -1                    Use data format v1, Simple Parity
  -2                    Use data format v2, Cooler Parity.
  						Note: This doesn't work yet
  -c, --check-file      Check for issues instead of instead of create
  -d, --dont-backup     By default this makes a backup of the file before
                        creating a dd2op file. This will cause it not to.
  -f, --fix-file        Fix any errors found durring a check, has no effect if
                        -c argument is not used
  -s block-length, --block-size block-length
                        Block size of parity blocks
  --hash-type {md5,sha128,sha256,sha512}
                        EOF checksum type (MD5, SHA128, SHA256, SHA512)
                        Defaults: SHA512

