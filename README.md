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
