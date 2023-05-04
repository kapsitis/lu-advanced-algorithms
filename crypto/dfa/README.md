# DFA (Differential Fault Analysis)

**Golden input:**

```
input FFFFFFFFFFF8974234: value0, value1, ... value1045, value1046 = 9, ... , value7451, 
output_orig (golden output) = 891241982479812471241
```

The goal is to recover round_key_10.
We introduce a fault:

```
input FFFFFFFFFFF8974234: value0, value1, ... value1045, value1046 = 0, ... , value7451, 
output_changed = 438753498753498573495
```

* Let's assume we introduced a fault just before last MixCol operation.
  [https://blog.quarkslab.com/differential-fault-analysis-on-white-box-aes-implementations.html]

* Public tools:
  [JeanGrey (DFA tool)](https://github.com/SideChannelMarvels).

Our first defense against DFA:

```
first_rounds last_three_rounds_0, last_three_rounds_1, output = 2 * last_three_rounds_0 - last_three_rounds_1
```

Task 2 Implement this basic variant of DFA that breaks your AES128 Encrypt.

* **input:** golden_output, some amount of faulty outputs
* **output:** the guessed round_key_10
* Also the original key?


## The 

* [NPTEL: Fault Attacks on AES](https://youtu.be/4cGXYxSd_s4)
* [Dmitry Khovratovich (Lux, 2016): First cryptanalysis of the full AES](https://youtu.be/Iw3gJNCq6go). 
* [Jakub Breier; Fault Attacks Made Easy: Differential Fault Analysis Automation on Assembly Code, 2018](https://youtu.be/yAVZbrTu2yo)

At round 9, after MixColumns:
DFA normal state[9] = 64fb242c867d9c25f1007f949f7afb9f
64. 86. F1. 9F.
FB. 7D. 00. 7A.
24. 9C. 7F. FB.
2C. 25. 94. 9F.
    
At round 9, after MixColumns:
DFA faulty state[9] = 65fb242c867d9c25f1007f949f7afb9f
65. 86. F1. 9F.
FB. 7D. 00. 7A.
24. 9C. 7F. FB.
2C. 25. 94. 9F.
    
Ciphertext with no fault:
E8. B3. 06. CC.
00. F4. 84. 1D.
27. 10. 53. 37.
FC. 77. 41. 1C.

Returning ciphertext: 
FA. B3. 06. CC.
00. F4. 84. F7.
27. 10. C2. 37.
FC. AB. 41. 1C.
        

[0x1., 0x1b., 0x27., 0x4b., 0x52., 0x5f., 0x60., 0x6b., 0x90., 0xa9., 0xaa., 0xc4., 0xcb., 0xd5., 0xfc.]
[0x2., 0xa., 0x32., 0x3d., 0x43., 0x46., 0x5c., 0x66., 0x8f., 0x9d., 0xa3., 0xb2., 0xb6., 0xd7., 0xe9.]


## Input format

```
[normal output]
[col0]
[faulty output1]
[faulty output2]
[col1]
[faulty output1]
[faulty output2]
[col2]
[faulty output1]
[faulty output2]
[col3]
[faulty output1]
[faulty output2]
```

## Output format

```
Round 10 Key: [round_key_10]
```

If some bytes were not guessed in a unique way, replace them by asterisks. 
After that list their possible values: 

```
Round 10 Key: de**be20****8d9cc8e43884526354**
Possible values:
Byte 1:  [00, 01, 02, ..., fd, fe, ff]
Byte 4:  [00, 01, 02, ..., fd, fe, ff]
Byte 5:  [00, 01, 02, ..., fd, fe, ff]
Byte 15: [00, 01, 02, ..., fd, fe, ff]

```





## Assumptions

1. Currently algorithm uses 1 normal output (128 bits) and 8 faulty outputs (128 bits each). 
   There are 2 faulty outputs per each column in the state matrix. 
   Having just one fault would reduce the number of candidate bytes (for K10 - the key in Round 10)
   to about 15. This does not allow to find the key byte uniquely.    
2. All faults happen only in the first row of the column. 
3. If there are two faults ("A + Delta1", "A + Delta2"), the difference of the added bytes 
   "Delta1 - Delta2" is never used, as it may be unknown in obfuscated situations.
4. Only encryption is covered by the current algorithm, but DFA technically doable for decryption as well.
5. The faults are always inserted immediately before the last MixColumns operation. 
   Inserting them a few stages earlier could also be doable.
   
## Observations

1. One should filter by Z (can do all offsets 0,7,10,13). 
   After that can use the feasible Z values to compute Y. 
   
   (Filtering by Y0, then by Z does not allow to eliminate anything. 
   The equation    
(nothing gets rejected this way). 


```
# Fault #1  (0x5c, 0xcd, 0xe7)
0x01: [[0x5c, 0x5e], [0xdd, 0xde], [0x28, 0x29], [0x56, 0x57]]
0x6b: [[0x1b, 0xcd], [0x57, 0xea], [0x95, 0xfe], [0x38, 0x53]]
0x90: [[0xdc, 0xe7], [0x69, 0xc2], [0x13, 0x83], [0x25, 0xb5]]

# Fault #2
0x02: [[0x58, 0x5c], [0xdb, 0xdd], [0x29, 0x2b], [0x55, 0x57]]
0x5c: [[0x75, 0xcd], [0x61, 0x85], [0x30, 0x6c], [0x20, 0x7c]]
0x9d: [[0xc6, 0xe7], [0x65, 0xd9], [0x35, 0xa8], [0x73, 0xee]]

Yi bytes
5c****** ******dd ****29** **57****

O (ciphertext output)
e80027fc b3f41077 06845341 cc1d371c

K0  = 0xa2
K7  = 0xb6
K10 = 0xf6
K13 = 0x46

Actual AES key
a295523f 83de61b6 1faff62c 0d466801
```

