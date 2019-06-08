# Extract information from the Egyptian National ID

EG national id is 14 digit ex(29501023201952) it could divide as described below

`2 - 990115 - 01 - 0192 - 1` 

`x - yymmdd - ss - iiig - z`

**x (2)** is the birth century (2 represent 1900 to 1999, 3 represent  2000 to 2099 .. etc)

**yymmdd (200115)** is the date of birth, yy(20) year,mm(01) month, dd(15) day 

**ss(01)**  birth governorate coda (88 for people who born in a foreign country, 01 for who born in Cairo, ...etc )

**iiig(0192)** the sequence in the computer between births in this birthday and 

**g(2)** represent the gender (2,4,6,8 for females and 1,3,5,7,9)

**z(1)** number  Ministry of Interior  added it to validate if the National ID fake or not (1 to 9)

script usage
`usage: extractor.py [-h] national_id`
