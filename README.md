DDOP
====

OP'd DD, is the DD/binary format but with some serious improvements. It inherits some general design considerations from the ubiquitious Encase format v1.

It suppports the following:
	Individual Block Integrity
	Multiple hashing formats to insure data integrity.
	Encryption of the datablocks
	[...]

Data Format:
 --------------------------------------------------------------------------------------------------
 | Header Information | Data Block | Checksum | Data Block | Checksum | [Repeat] | Final Checksum |
 --------------------------------------------------------------------------------------------------


Supported Hashing Types:
	md5
	sha256
	sha512
	md5+sha256
	md5+sha512
	sha256+sha512

Usage:
	dd2op [options] file.bin cool_file.ddop
	
	Options:
		-h, --help
			Prints this help Menu
		-t, --block-checksum-type <type>
			Hash the datablocks using one of the allowed hashing types (md5, sha256, sha512)
			Default: md5
		-f, --final-checksum-type <type>
			Hash of the entire file upto the final checksum section using one of the allowed hashing types.
			Default: sha512
		-c, --compress-datablocks
			Compress the data blocks prior to writing them out
		--compress-everything
			Compress everything after the header information prior to writing to disk.
		-e, --encrypt-datablocks <type> <password>
			Encrypt the data blocks using some form of encryption and with the specified password.
		--encrypt-everything <type> <password>
			Encrypt everything after the header information prior to writing the file to disk. 
	
	op2dd [options] cool_file.ddop file.bin
		Works the same way as dd2op except in reverse.
	