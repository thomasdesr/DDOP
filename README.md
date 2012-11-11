#DDOP

dd2op, because dd is way too OP’d as a forensics format. It, like every other
format has has a problem. That being in cases of bit flips in the storage or
transmission medium  whole chunk of data is lost. The goal of this format is
to allow for the recovery of stored data. This is accomplished by adding parity
to the data.


##Data Format v1:

    +------------------------------------------------------------------------------+
    ¦ Data Block ¦ Parity ¦ Data Block ¦ Parity ¦ [Repeat] ¦ Final Check-sum Block ¦
    +------------------------------------------------------------------------------+

While this format can allow for the recovery of data, it has no ability to
detect if there has been corruption of the parity valueswhich could allow for
additional corruption of data. Although as long as the final checksum block
remains unaffected, it is possible for recovery to occur by brute forcing
flipped bits and by treating all three bits as malformed data. This is however
not how parity is supposed to work and is really a workaround until Data
Format v2 can be fully implemented.



##Dava Format v2:

    +-------------------------+
    ¦ Data Block ¦ Parity bit ¦
    +-------------------------+
    ¦ Data Block ¦ Parity bit ¦
    +-------------------------+
    ¦         [Repeat]        ¦
    +-------------------------+
    ¦  Vertical Parity Values ¦
    +-------------------------+
    ¦  Final Check-sum Block  ¦
    +-------------------------+

Data Format v2 is where this actually really turns into a parity data recovery
format. With the addition of the horizontal and vertical parity it makes it
truly able to recover data with a reasonable degree of certainty.


##Examples:
1. Basic Usage
    ```
    $ dd2op -1 example_file.bin  
    7061192b80701d2b19ecd9e373db68ead4cdaebc92e7ac99b0f26137c1ca7b2b5aff809ff9fda24a941b7d8a4df4e23956f5f1e4d42485da152644c82a4162a1
    ```

    _This will create a dd2op file called example_file.bin.dd2op. The output is the (EOF) hash for the file. 
Note that the default EOF hashing algorithim is sha512._


2. Setting a different EOF hash type
    ```
    $ dd2op --hash-type md5 example_file.bin
    183b605a1eb1059b371ebf892237073a
    ```

3. Setting a different block/chunk size
    ```
    $ dd2op -s 64 --hash-type md5 example_file.bin
    8d0d603081614dd6f204db8a4b8343fe
    $ dd2op --block-size 64 --hash-type md5 64 example_file.bin
    8d0d603081614dd6f204db8a4b8343fe
    ```

    _This sets the block size for both reading in the file and creating the parity blocks, this means a lot more in file format v1 than v2._
    
4. File Checking
    ```
    $ dd2op -c -2 example_file.bin.dd2op
    dd2op: Final Checksum Check -> Passed
    dd2op: Horizontal Parity Check -> Passed
    dd2op: Vertical Parity Check -> Passed
    dd2op: (3/3) Checks passed, file is dd2op approved!
    ```
    
    _This option will check the file to see if there are any signs of corruption. This example uses file format v2, however v1 looks simlar._



    

