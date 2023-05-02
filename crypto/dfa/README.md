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