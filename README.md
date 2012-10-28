DDOP
====

OP'd DD, is classic DD/binary format but with some serious improvements. It inherits some design considerations from the ubiquitious Encase format v1.

It suppports the following:
	Individual Block Integrity
	Multiple hashing formats to insure data integrity.
	[...]

Data Format:
 --------------------------------------------------------------------------------------------------
 | Header Information | Data Block | Checksum | Data Block | Checksum | [Repeat] | Final Checksum |
 --------------------------------------------------------------------------------------------------
                      [        Chunk 1        ]
                      [                   Chunk 2                    ]


