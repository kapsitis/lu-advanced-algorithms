---
layout: default
title: "Error Correction: Hamming Codes"
lang: en
permalink: /lectures/lossy_hamming/en/
---
# 7. Error Correction: Hamming Codes

**Goals**

* Introduce a few popular error detection algorithms.
* Justify a claim about the distance between two error-correcting codewords.
* Use and justify Hamming codes.

**Error detection:**

![Error detection](figs/error-detection.png)

**Error correction:** The idea behind all methods is to add extra information to the transmitted data, hoping that the extra information will make it possible to notice errors.

![Error correction](figs/error-correction.png)

## Error Detection Algorithms

For error detection, a short *checksum* is added to the data; the receiver recomputes it and compares. The parity bit and CRC are designed for random transmission errors (noise). If the data may have been changed on purpose, a *cryptographic hash function* (e.g., SHA-256) is needed, for which an attacker cannot forge a matching new value.

### Parity Bit

**The bit parity method:** We transmit an $n$-bit string $x_1,x_2,\ldots,x_n \in \lbrace 0; 1 \rbrace$. To detect a possible error in 1 bit (which may or may not happen), we transmit $n+1$ bits: all of $x_1,x_2,\ldots,x_n$ and also the last bit

$$
\left( x_1 + x_2 + \ldots + x_n \right)\,\text{mod}\,2.
$$

The last bit stores the parity of all the previous bits. Therefore the parity of all $n+1$ bits is $0$. If one error occurs during transmission, the parity will be $1$, and the error can be detected.

### CRC Checksum

*CRC* (*cyclic redundancy check*) treats a bit string as the coefficients of a polynomial modulo $2$. The sender divides the message polynomial $M(x)$, multiplied by $x^{32}$, by a fixed *generator polynomial* $G(x)$ (of degree $32$) and appends the remainder of the division -- $32$ bits -- to the message. Long division modulo $2$ consists only of shifts and XOR, so CRC is very fast to compute both in software and in hardware. Ethernet uses CRC-32 with

$$
G(x) = x^{32} + x^{26} + x^{23} + x^{22} + x^{16} + x^{12} + x^{11} + x^{10} + x^{8} + x^{7} + x^{5} + x^{4} + x^{2} + x + 1
$$

(`0x04C11DB7` in hexadecimal). The receiver computes the CRC of the whole frame together with the checksum; for a correct frame the result is always the same constant `0xC704DD7B` (`0xDEBB20E3` in bit-reversed notation), the so-called "magic number".

CRC-32 is guaranteed to detect any single-bit error and any error burst that spans at most $32$ adjacent bits -- such errors occur, for example, during short interference. It misses random corruption with probability about $2^{-32}$.

**Efficient computation.** Long division can be carried out one bit at a time: a $32$-bit register holds the current remainder; at each step it is shifted, and if a one "falls out" of the register, the generator polynomial is added (XOR). In hardware (a network card) this is a shift register with a few XOR gates. In software it is better to process a whole byte at once: the effect of each byte on the register ($8$ division steps) is precomputed and stored in a table of $256$ entries. Practical CRC-32 has three more details:

* Ethernet transmits each byte starting with the least significant bit, so the register holds the bits in reversed order: it is shifted to the right, and the generator polynomial is `0x04C11DB7` with reversed bits, i.e., `0xEDB88320`.
* The initial value of the register is `0xFFFFFFFF` (not $0$), so that the CRC changes also when zero bytes are added to or removed from the beginning of the message.
* At the end the result is inverted (XOR with `0xFFFFFFFF`), so that zeros appended at the end also change the CRC.

$\textsf{CRC32-Make-Table}()$ $\quad$ *// $T[n]$ -- the effect of byte $n$ on the register after $8$ steps*
1. **for** $n = 0$ **to** $255$
2. $\quad c = n$
3. $\quad$ **for** $k = 1$ **to** $8$ $\quad$ *// one division step for each bit*
4. $\quad\quad$ **if** $c$ is odd $\quad$ *// a one falls out of the register*
5. $\quad\quad\quad c = (c \gg 1) \oplus \mathtt{0xEDB88320}$
6. $\quad\quad$ **else** $c = c \gg 1$
7. $\quad T[n] = c$
8. **return** $T$

$\textsf{CRC32}(B, n, T)$ $\quad$ *// $B[1:n]$ -- the bytes; $T$ -- the result of $\textsf{CRC32-Make-Table}$*
1. $c = \mathtt{0xFFFFFFFF}$
2. **for** $i = 1$ **to** $n$
3. $\quad c = T[(c \oplus B[i]) \wedge \mathtt{0xFF}] \oplus (c \gg 8)$ $\quad$ *// $8$ division steps at once*
4. **return** $c \oplus \mathtt{0xFFFFFFFF}$

Here $\oplus$ is bitwise XOR, $\gg$ is a right shift, and $\wedge$ is bitwise AND (after $\wedge \mathtt{0xFF}$ only the lowest byte remains). In line 3, the lowest byte of the register together with the next message byte selects a table entry that describes the effect of these $8$ division steps on the remaining bits of the register. So each byte needs one XOR, one table lookup ($256$ words, $1$ KiB) and one shift: the time is $O(n)$, about $8$ times faster than processing bit by bit. For testing: $\textsf{CRC32}$ of the string `123456789` is `0xCBF43926`. (Even faster implementations use several tables and process $4$ or $8$ bytes at a time, or use processor instructions: ARMv8 has dedicated CRC-32 instructions, x86 has carry-less multiplication PCLMULQDQ.)

If $\textsf{CRC32}$ is run over the whole frame together with the FCS, then for a correct frame the register before the final XOR always contains `0xDEBB20E3` -- this is the same "magic number" `0xC704DD7B`, only with reversed bits (see Problem 7.6).

<img
  id="ethernet_kadrs"
  alt="Ethernet frame and checksums"
  src="{{ '/lectures/lossy_hamming/figs/ethernet-frame.en.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*An Ethernet II frame and the contents of its data field (an IPv4 packet with a TCP segment). The length of each field in bits is shown below it; bit numbers in the headers are counted from $0$. The widths of the fields in the figure are not proportional to their lengths.*

Checksums appear in several protocol layers:

* **Data link layer** (OSI layer 2): the last field of an Ethernet frame, FCS (*Frame Check Sequence*, $32$ bits), is the CRC-32 from the destination address to the end of the data field. It is computed and checked by the network card; a frame with a wrong FCS is simply dropped (not requested again). Wi-Fi frames have the same CRC-32.
* **Network layer** (IPv4): the header checksum ($16$ bits) protects only the IP header, because routers change it (for example, they decrement the TTL). IPv6 no longer has this checksum.
* **Transport layer** (TCP): the checksum ($16$ bits) protects the TCP header, the data and the IP addresses. The IP and TCP checksums are sums of $16$-bit words with end-around carry (the *Internet checksum*) -- much weaker than CRC-32, but they check the data along the whole path from the sender to the receiver. If a segment is lost (also because some frame was dropped), TCP notices this from the sequence numbers and missing acknowledgments and sends it again.

CRC-32 is also used in file formats (ZIP, gzip, PNG); other CRC variants appear in USB, CAN and many other communication protocols.

CRC does not protect against deliberate changes: CRC is linear, and anyone who has changed the data can also compute the new checksum.

### MD5

MD5 (R. Rivest, 1992) is a hash function that computes a $128$-bit value for an input of any length (written as $32$ hexadecimal digits). The algorithm is described in [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321); its structure is similar to SHA-256 (see the next subsection: $512$-bit blocks and a compression function with $64$ steps). MD5 **must not** be used for cryptographic purposes:

* **Identical-prefix collisions.** In 2004 the group of Wang Xiaoyun found the first MD5 collision -- two different messages with the same MD5 value. Today an ordinary computer finds such a pair (with any chosen common beginning) in seconds. An attacker can prepare two documents with the same MD5 -- a harmless one and a harmful one --, get the harmless one signed, and the signature will also be valid for the harmful one.
* **Chosen-prefix collisions.** In 2007 M. Stevens, A. Lenstra and B. de Weger showed how to extend two *arbitrary* given beginnings so that their MD5 values coincide. In 2008, $200$ PlayStation 3 consoles took a few days to create a rogue certificate authority (CA) certificate, and in 2012 the *Flame* malware used such a collision to forge a Microsoft code signature. Today a few GPU days are enough.
* **Preimages are still out of reach.** Given an MD5 value (not created by the attacker), finding an input with this value takes about $2^{123}$ operations with the best known attack -- practically impossible. Collisions can only be created for pairs of messages that the attacker constructs.
* **Passwords.** MD5 is very fast (a graphics card computes tens of billions of values per second), so MD5 values of passwords are easy to find by exhaustive search (see "Short Inputs and Dictionary Attacks").

MD5 can still be useful for detecting random corruption, but even for that SHA-256 is a better choice.

### SHA-256

*SHA-256* is a hash function of the SHA-2 family, defined by the US standard NIST FIPS 180-4 (first version in 2001). The input is any bit string of length $L < 2^{64}$; the output is always $256$ bits ($64$ hexadecimal digits). For example, the SHA-256 value of the string `abc` is `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`.

<img
  id="sha256_shema"
  alt="SHA-256 computation"
  src="{{ '/lectures/lossy_hamming/figs/sha256-diagram.en.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*SHA-256 computation; the numbers match the steps listed below. The numbers in the example are real.*

1. **Padding.** A bit $1$ is appended to the message, then as many zeros as needed, and at the end the message length $L$ as a $64$-bit number, so that the total length is a multiple of $512$.
2. **Splitting into blocks** $M_1, \ldots, M_N$ of $512$ bits.
3. **Chain of compression functions.** The state consists of $8$ words of $32$ bits; the initial value $H_0$ is fixed (the first $32$ bits of the fractional parts of the square roots of the first $8$ primes). Each block updates it: $H_i = f(H_{i-1}, M_i)$. The function $f$ expands the $16$ words of the block to $64$ words and in $64$ rounds changes the state with logical functions, bit rotations, constants (the fractional parts of the cube roots of the first $64$ primes) and addition modulo $2^{32}$.
4. **The result** is the last state $H_N$.

**Properties of a cryptographic hash function.** Computing SHA-256 is deterministic and fast, and it has the following properties:

* *preimage resistance*: given a value $h$, one cannot find $m$ with $\text{SHA-256}(m) = h$ -- the best known method is exhaustive search with about $2^{256}$ attempts;
* *second preimage resistance*: given $m$, one cannot find another $m' \neq m$ with the same value (also about $2^{256}$ attempts);
* *collision resistance*: one cannot find any pair $m \neq m'$ with equal values (about $2^{128}$ attempts, see below);
* *avalanche effect*: when one input bit changes, each output bit changes with probability $\frac{1}{2}$. For example, the value `a52d159f262b2c6d…` of `abd` is nothing like the value of `abc`.

**The collision paradox.** There are infinitely many input strings (there are already $2^{257}$ strings of $257$ bits), but only $2^{256}$ output values. By the pigeonhole principle, collisions **certainly exist**, and there are very many of them. Still, not a single SHA-256 collision is known, because no way is known to find one faster than by random search. When inputs are chosen at random, by the *birthday paradox* the first collision is expected after about $\sqrt{2^{256}} = 2^{128} \approx 3.4 \cdot 10^{38}$ attempts. Even the entire Bitcoin network (about $10^{21}$ SHA-256 computations per second) would spend about $10^{10}$ years on this -- roughly the age of the Universe. So the security is not mathematically proven; it rests on the fact that long-term analysis has not found a faster method.

**Why SHA-256 is the industry standard.** After more than $20$ years of cryptanalysis there are no known practical attacks on the full SHA-256 (attacks only work on versions with a reduced number of rounds). It is fast, recent Intel, AMD and ARM processors have dedicated instructions for it, and many standards require it. The previous standard SHA-1 is broken (the first SHA-1 collision, *SHAttered*, was published in 2017), so systems moved to SHA-256. An alternative is SHA-3 (2015), which is based on different principles.

Applications:

* **Cryptocurrencies.** A Bitcoin block header contains the hash of the previous block, so the history cannot be rewritten without recomputing all subsequent blocks. Proof of work: miners search for a block header whose double SHA-256 value is below a given threshold. The transactions are summarized in the block header by a Merkle tree of SHA-256 values, and addresses are derived from the public key with SHA-256 and RIPEMD-160. (Ethereum uses Keccak-256 instead of SHA-256.)
* **Certificates and signatures:** TLS (HTTPS) certificates and software and document signatures sign not the document itself but its SHA-256 value.
* **Data integrity:** checksums of downloaded files (`sha256sum`), Docker image identifiers, package managers; the version control system Git supports repositories with SHA-256 (by default it still uses SHA-1).
* **Message authentication** (HMAC-SHA256, e.g., in JWT tokens and in signatures of cloud service API requests) and key derivation.

**SHA-256 in a post-quantum world.** Quantum computers would break RSA and elliptic-curve signatures (Shor's algorithm), but for hash functions they give only a quadratic speedup: Grover's algorithm reduces a preimage search from $2^{256}$ to about $2^{128}$ quantum operations, which is still infeasible. Theoretical quantum collision algorithms would need a huge quantum memory and are practically not faster than the classical $2^{128}$. Therefore SHA-256 is considered secure in the post-quantum era as well; post-quantum signature standards are even built from hash functions (SLH-DSA, or SPHINCS+, NIST FIPS 205, 2024). If a larger margin is needed, SHA-384 or SHA-512 is used.

### Short Inputs and Dictionary Attacks

A hash function does not hide its input if there are few possible inputs. Passwords, PIN codes, phone numbers or personal identity numbers are such inputs: the attacker simply computes SHA-256 for all candidates (a dictionary or all possibilities) and compares. A graphics card computes tens of billions of SHA-256 values per second, so, for example, all $10^8$ eight-digit numbers are checked in a fraction of a second. Without additional measures the attacker can also precompute tables (*rainbow tables*) for all the most common passwords.

Therefore short or predictable inputs are not hashed directly but are concatenated with additional data:

* **Salt:** a separate random number for each record (e.g., $16$ bytes), stored together with the result: $h = \text{SHA-256}(\textit{salt} \,\|\, \textit{password})$. Equal passwords give different values, precomputed tables become useless, and each record has to be attacked separately.
* **Pepper:** a secret value added to all inputs but stored separately from the database (e.g., in a hardware security module). Without it a stolen database is useless.
* **Slow hashing** (*key stretching*): SHA-256 is too fast for storing passwords. Functions that deliberately require a lot of work or memory are used instead: PBKDF2-HMAC-SHA256 with hundreds of thousands of iterations, bcrypt, scrypt or Argon2 (the winner of the 2015 Password Hashing Competition). The user does not notice this, but exhaustive search becomes hundreds of thousands of times slower.
* **Secret key:** if the hash is to show that the message was sent by the owner of a key, HMAC is used instead of a plain $\text{SHA-256}(\textit{key} \,\|\, \textit{message})$. In the latter case an attacker can append a continuation to the message of a valid value without knowing the key (*length extension*), because the SHA-256 result is the state $H_N$ itself, from which the chain can be continued.

## Concepts of Error Correction Algorithms

**Example (Triple repetition):**

![Triple repetition](figs/repetition-code.png)

Each transmitted bit is repeated three times. The receiver finds which bit occurs more often -- zeros or ones. Such a code can correct an error in one bit.

**Definition:** An *error-correcting code* is called an $[n,k,d]$-code if

* $n$ is the number of bits the encoding actually transmits,
* $k$ is the number of bits being encoded,
* $d$ is the number of errors that can be corrected.

**Example:** For the triple repetition method $n=3$, $k=1$, $d=1$, so it is a $[3,1,1]$-code.

**Negative example:** We want to build an error-correcting code for an alphabet with $3$ messages: $A = \lbrace a,b,c \rbrace$. We propose to encode the messages $a,b,c$ with the codes $S = \lbrace \mathtt{1000},\mathtt{0101},\mathtt{1101} \rbrace$, respectively.

This code cannot correct one error: on receiving the string `0101` it is unclear whether the string `0101` was sent (without errors) or the string `1101` (with one error -- in the first bit). `1001` and others are ambiguous as well.

### Properties of Error-Correcting Codes

**Theorem:** A set $S$ of message codes is an $[n,k,d]$-code if and only if

1. $S$ consists of strings of length $n$,
2. $\lvert S \rvert \geq 2^k$, so that there are enough codes for all $k$-bit strings,
3. any two strings of $S$ differ in at least $2d+1$ positions.

**Proof:** The code cannot correct $d$ errors if there is a string $z = z_1z_2\ldots{}z_n$ and two strings of the set, $x=x_1x_2\ldots{}x_n$ and $y=y_1y_2\ldots{}y_n$, each of which differs from $z$ in at most $d$ positions. Then the strings $x$ and $y$ differ in at most $2d$ positions. Therefore, for the code to be able to correct errors, any two strings of $S$ must differ in at least $2d+1$ positions.

**Example ($n=3$):** If the number of transmitted bits is $n=3$ and the maximum allowed number of errors is $d=1$, then the set $S$ cannot contain more than two strings. If $x_1x_2x_3 \in S$, then the only other string can be $y_1y_2y_3$ with $y_1 \neq x_1$, $y_2 \neq x_2$, $y_3 \neq x_3$.

**Corollary:** There is an $[n,k,d]$ code $[3,1,1]$ that transmits $k=1$ content bit in $n=3$ bits and can correct up to $d = 1$ error. More than $k=1$ bit (i.e., more than two distinguishable strings) cannot be transmitted.

**Claim:** Even when $n=4$ bits are transmitted, no more than two strings can be encoded (so that they are distinguishable when there is at most $d=1$ error).

**Proof:** Suppose the opposite and consider three strings of the set $S$: $x_1x_2x_3x_4$, $y_1y_2y_3y_4$ and $z_1z_2z_3z_4$. No two strings can agree in more than one position. Hence the total number of agreements cannot exceed $3$.

If all three bits agreed in some position $i$ ($x_i = y_i = z_i$), we would get a contradiction: all three agreements would already be used up, but there must be agreements in the other positions $j \neq i$ as well, since there are three numbers $x_j$, $y_j$, $z_j$ and only two values.

If two bits agree and the third one differs, the number of agreements in this bit is 1. Since there are 4 bits, the total number of agreements is at least 4, which contradicts the fact that it cannot exceed 3.

Therefore the set $S$ cannot contain more than two strings. $\blacksquare$

**Example ($n=5$, $k=2$):**

| $x_1$ | $x_2$ | $x_1,x_1,x_2,x_2,(x_1 + x_2)\,\text{mod}\,2$ |
| --- | --- | --- |
| 0 | 0 | 00000 |
| 0 | 1 | 00111 |
| 1 | 0 | 11001 |
| 1 | 1 | 11110 |

The table shows how to encode two-bit strings as five-bit strings: the first bit is transmitted twice, the second bit twice, and the last bit is the parity of both content bits.

*Note:* The table shows a $[5,2,1]$-code.

**Can there be more than 4 strings when $n=5$?**

**Claim:** For $n=5$ and $d=1$ the set $S$ cannot contain more than four strings.

**Proof:** Suppose the opposite and consider five strings of the set $S$. At least three of them have the same first bit, i.e., either at least $3$ strings have the first bit $0$, or at least $3$ strings have the first bit $1$.

These three strings can differ only in the last four bits. But for four bits we have already proved that at most $2$ strings are distinguishable. Therefore some two of these three strings differ in fewer than three positions. A contradiction. $\blacksquare$

## Hamming Codes

**If $n=7$ bits are transmitted:** From $n=7$ bits one can build $2^4 = 16$ distinguishable strings (in lexicographic order):

```text
0000000
0000111
0011001
0011110
0101010
0101101
0110011
0110100
1001011
1001100
1010010
1010101
1100001
1100110
1111000
1111111
```

**Constructing the Hamming code:** The string $x_1x_2x_3x_4$ is transmitted as $x_1x_2x_3y_1x_4y_2y_3$, where

$$
\begin{array}{l}
y_1 = \left( x_1 + x_2 + x_3 \right)\,\text{mod}\,2\\
y_2 = \left( x_1 + x_2 + x_4 \right)\,\text{mod}\,2\\
y_3 = \left( x_1 + x_3 + x_4 \right)\,\text{mod}\,2\\
\end{array}
$$

This is a $[7,4,1]$-code, also called the *Hamming code*.

**Claim (about the Hamming code $[7,4,1]$):** Any two 7-bit strings of the Hamming code differ in at least $3$ positions (so one error can be corrected).

**Proof:** Consider any two correctly computed (received without errors) strings $x_1x_2x_3y_1x_4y_2y_3$ and $x'_1x'_2x'_3y'_1x'_4y'_2y'_3$.

**Case 1:** One $x_i$ differs. Each $x_i$ appears in at least $2$ of the formulas for $y_1$, $y_2$, $y_3$, and when the value of $x_i$ changes, the values of these formulas change. Therefore the strings differ in at least $3$ positions: in one $x_i$ and in at least two $y_i$.

$$
\begin{array}{l}
y_1 = \left( x_1 + x_2 + x_3 \right)\,\text{mod}\,2\\
y_2 = \left( x_1 + x_2 + x_4 \right)\,\text{mod}\,2\\
y_3 = \left( x_1 + x_3 + x_4 \right)\,\text{mod}\,2\\
\end{array}
$$

**Case 2:** Two $x_i$ differ. Denote the differing bits by $x_i$ and $x_j$. Whatever $i$ and $j$ are, we can always find one of the $y_i$ formulas that contains one of $x_i$ and $x_j$ but not the other. The strings differ in at least $3$ positions: in the two $x_i$ and in this one $y_i$.

**Case 3:** Three $x_i$ differ. Then there are immediately $3$ differences in these $x_i$ (since they are also transmitted themselves). $\blacksquare$

**Hamming code: the general case.** A Hamming code consists of strings of $2^n-1$ bits, in which $2^n-n-1$ bits are used for the message and $n$ are check bits computed from the message bits.

To describe this code, we number the $2^n-1$ bit positions with the numbers $1, 2, \ldots, 2^n-1$, written in binary ($000001$, $000010$, $\ldots$, $111111$). There are $n$ numbers whose binary representation contains exactly one $1$ ($000001$, $000010$, $\ldots$, $100000$). The check bits are placed in these positions.

The remaining positions are message bits, which can be arbitrary.

**Examples:** The generalized Hamming code can be described as $\left[ 2^n - 1, 2^n - n - 1,1 \right]$. For all values of $n$ it corrects only $1$ bit.

* $n = 2$: the Hamming code $[3,1,1]$ (triple repetition).
* $n = 3$: the Hamming code $[7,4,1]$.
* $n = 4$: the Hamming code $[15,11,1]$.
* $n = 5$: the Hamming code $[31,26,1]$.
* $n = 6$: the Hamming code $[63,57,1]$.

**Computing the check bits**

$$
x_{0\ldots{}010\ldots{}0} = \left(
\sum\limits_{i_1,\ldots,i_{k-1},i_{k+1},\ldots,i_{n}}
x_{i_1\ldots{}i_{k-1}1i_{k+1}\ldots{}i_n} \right)\;\text{mod}\;2
$$

To find out whether there is an error, we proceed as follows. If the check bit in position $0\ldots{}010\ldots{}0$ (with a 1 in the $k$-th digit) **does not match** the value computed by the formula, then we know that one of the bits whose number has a $1$ in the $k$-th position is wrong.

If the check bit in position $0\ldots{}010\ldots{}0$ (with a 1 in the $k$-th digit) **matches** the value computed by the formula, then the error can only be in the bits whose numbers have a $0$ in the $k$-th position (because all bits with a 1 in the $k$-th position appear in the formula).

**Finding the error:** In this way each check bit determines one bit of the number of the position with the error. Together the check bits determine this position number completely. If the resulting number is $000\ldots{}000$ (i.e., all check bits matched), there is no error at all. Otherwise we know where it is.

What happens if the error is in a check bit itself?

**Theorem (optimality of the Hamming code):** If $S \subseteq \lbrace 0, 1 \rbrace^{2^n-1}$ is a code that can correct one error, then $\lvert S \rvert \leq 2^{2^n-n-1}$.

This theorem means that the number of strings in the Hamming code cannot be improved even by $1$ string!

**Proof:** Denote the codewords by $v_1,\ldots,v_m$. Let $V_i$ be the set containing $v_i$ and all strings that differ from $v_i$ in exactly one position (the "$\varepsilon$-neighborhood" of the codeword $v_i$).

1. The neighborhoods $V_i$ and $V_j$ ($i \neq j$) have no common elements; otherwise error correction would be impossible.
2. Each $V_i$ contains exactly $2^n$ strings: $v_i$ and $2^n - 1$ strings that differ from it in $1$ position.

Therefore the sets $V_1,V_2,\ldots,V_m$ together contain $2^n \cdot m$ elements. Since there are $2^{2^n - 1}$ strings of length $2^n-1$ in total,

$$
2^n \cdot m \leq 2^{2^n - 1} \Rightarrow m \leq 2^{2^n - n-1}.
$$

$\blacksquare$

## Other Linear Codes

**Definition:** Any code in which each bit of the encoded string can be described by a formula

$$
\left( x_{i_1} + \dots + x_{i_k} \right)\,\text{mod}\,2
$$

is called a linear code. The Hamming code is a linear code, and almost all other codes used in practice are linear as well.

A linear code can be described by its generator matrix. If $n$ is the length of the encoded message and $k$ is the number of bits being encoded, then the generator matrix is an $n \times k$ matrix. If bit $x_i$ appears in the formula for the $j$-th bit of the encoded message, then position $(i,j)$ of this matrix contains $1$. Otherwise it contains $0$.

**Example (linear code):** The generator matrix of the Hamming code $[7,4,1]$ looks as follows:

$$
G = \left(
\begin{array}{cccc}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
1 & 1 & 1 & 0 \\
0 & 0 & 0 & 1 \\
1 & 1 & 0 & 1 \\
1 & 0 & 1 & 1
\end{array} \right)
$$

Rows 1, 2, 3 and 5 express that bits of the encoded message coincide with bits of the original message. The other rows describe the formulas for the check bits.

**Encoding a message:** To encode a message, we write it as a vector:

$$
\mathbf{x} = \left( \begin{array}{l}
x_1\\
x_2\\
x_3\\
x_4
\end{array} \right)
$$

and then multiply this vector by the generator matrix $M$. The encoded message is $G\mathbf{x}$, with all its elements computed modulo $2$.

**Decoding a linear code:** Decoding can use the parity-check matrix. For the Hamming code $[7,4,1]$ it is:

$$
P = \left( \begin{array}{ccccccc}
1 & 1 & 1 & 1 & 0 & 0 & 0\\
1 & 1 & 0 & 0 & 1 & 1 & 0\\
1 & 0 & 1 & 0 & 1 & 0 & 1
\end{array} \right)
$$

Each row of the table describes one of the checks of the Hamming code (whether a check bit matches a certain sum of bits modulo $2$).

If $\mathbf{y}$ is the encoded message, $P$ is the parity-check matrix and there are no errors, then, computing modulo $2$,

$$
P\mathbf{y} = \left( \begin{array}{c}
0 \\
0 \\
0
\end{array} \right)
$$

The parity-check matrix can also be used to find where the errors are, if there are any, but this is more complicated and is not covered in this course.

## Hamming Code Examples

**7-bit Hamming code**

| $x,y$ notation | $x_1$ | $x_2$ | $x_3$ | $\textcolor{red}{y_1}$ | $x_4$ | $\textcolor{red}{y_2}$ | $\textcolor{red}{y_3}$ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Notation with binary indices | $\textcolor{blue}{x_{111}}$ | $\textcolor{blue}{x_{110}}$ | $\textcolor{blue}{x_{101}}$ | $\textcolor{blue}{x_{100}}$ | $\textcolor{blue}{x_{011}}$ | $\textcolor{blue}{x_{010}}$ | $\textcolor{blue}{x_{001}}$ |

The codes $x_{111},\ldots,x_{001}$ are arranged in [reverse lexicographic order](https://oeis.org/wiki/Orderings#Reverse_lexicographic_order) - or simply in decreasing order.

Why are the message bits $x_i$ slightly mixed with the check bits $y_j$ in the string $x_1,x_2,x_3,y_1,x_4,y_2,y_3$?

$$
\left\{
\begin{array}{l}
y_{1} = \textcolor{blue}{x_{100}} = \textcolor{blue}{x_{111} \oplus x_{110} \oplus x_{101}} = x_1 \oplus x_2 \oplus x_3\\
y_{2} = \textcolor{blue}{x_{010}} = \textcolor{blue}{x_{111} \oplus x_{110} \oplus x_{011}} = x_1 \oplus x_2 \oplus x_4\\
y_{3} = \textcolor{blue}{x_{001}} = \textcolor{blue}{x_{111} \oplus x_{101} \oplus x_{011}} = x_1 \oplus x_3 \oplus x_4
\end{array} \right.
$$

By $x_1 \oplus x_2$ we denote $\left(x_1+x_2\right)\,\text{mod}\,2$: addition modulo $2$, or XOR, or "exclusive OR".

Examples of encoding and decoding with the Hamming code $[7,4,1]$ are in Problems 7.1-7.4.

## Problems

**Problem 7.1:** Encode the string `0110` with the Hamming code $[7,4,1]$.

**Answer:** We take $x_1 = 0$, $x_2 = 1$, $x_3 = 1$, $x_4 = 0$. Computing $y_1$, $y_2$, $y_3$ with the formulas

$$
\left\{
\begin{array}{l}
y_1 = x_1 \oplus x_2 \oplus x_3\\
y_2 = x_1 \oplus x_2 \oplus x_4\\
y_3 = x_1 \oplus x_3 \oplus x_4
\end{array} \right.
$$

gives $y_1 = 0$, $y_2 = 1$, $y_3 = 1$. So the encoded message is `0110011`. $\square$

**Problem 7.2:** Decode the string `0111101` with the Hamming code $[7,4,1]$.

**Answer:**

$$
\left\{
\begin{array}{l}
y_1 = x_1 \oplus x_2 \oplus x_3,\\
y_2 = x_1 \oplus x_2 \oplus x_4,\\
y_3 = x_1 \oplus x_3 \oplus x_4.
\end{array} \right.
$$

* $y_1$ does not match $\Rightarrow$ the error can only be in one of the bits that affect $y_1$ ($y_1, x_1, x_2, x_3$).
* $y_2$ matches $\Rightarrow$ the error can only be in one of the bits that do not affect $y_2$ ($y_1, y_3, x_3$).
* $y_3$ does not match $\Rightarrow$ the error can only be in one of the bits that affect $y_3$ ($x_1, x_3, x_4, y_3$).
* The only bit marked in all rows is $x_3$. So this is the wrong bit.

The original message was $\mathtt{01}\textcolor{red}{\mathtt{0}}\mathtt{1101}$ (and $x_1x_2x_3x_4 = \mathtt{0101}$).

An "X" in the $i$-th row means that the check bit $y_i$ allows an error in the corresponding bit.

| $x_1 = \mathtt{0}$ | $x_2 = \mathtt{1}$ | $x_3 = \mathtt{1}$ | $y_1 = \mathtt{1}$ | $x_4 = \mathtt{1}$ | $y_2 = \mathtt{0}$ | $y_3 = \mathtt{1}$ |
| --- | --- | --- | --- | --- | --- | --- |
| X | X | X | X | | | |
| | | X | X | | | X |
| X | | X | | X | | X |
| $\mathtt{0}$ | $\mathtt{1}$ | $\textcolor{red}{\mathtt{0}}$ | $\mathtt{1}$ | $\mathtt{1}$ | $\mathtt{0}$ | $\mathtt{1}$ |

$\square$

**Problem 7.3:** Decode the string `1010010` with the Hamming code $[7,4,1]$.

**Answer:**

$$
\left\{
\begin{array}{l}
y_1 = x_1 \oplus x_2 \oplus x_3,\\
y_2 = x_1 \oplus x_2 \oplus x_4,\\
y_3 = x_1 \oplus x_3 \oplus x_4.
\end{array} \right.
$$

* $y_1$ matches $\Rightarrow$ the error can only be in one of the bits that do not affect $y_1$ ($y_2, y_3, x_4$).
* $y_2$ matches $\Rightarrow$ the error can only be in one of the bits that do not affect $y_2$ ($y_1, y_3, x_3$).
* $y_3$ matches $\Rightarrow$ the error can only be in one of the bits that do not affect $y_3$ ($y_1, y_2, x_2$).
* No bit is marked in all rows. There are no wrong bits.

The original message was $\mathtt{1010010}$ (and $x_1x_2x_3x_4 = \mathtt{1010}$).

An "X" in the $i$-th row means that the check bit $y_i$ allows an error in the corresponding bit.

| $x_1 = \mathtt{1}$ | $x_2 = \mathtt{0}$ | $x_3 = \mathtt{1}$ | $y_1 = \mathtt{0}$ | $x_4 = \mathtt{0}$ | $y_2 = \mathtt{1}$ | $y_3 = \mathtt{0}$ |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | X | X | X |
| | | X | X | | | X |
| | X | | X | | X | |
| $\mathtt{1}$ | $\mathtt{0}$ | $\mathtt{1}$ | $\mathtt{0}$ | $\mathtt{0}$ | $\mathtt{1}$ | $\mathtt{0}$ |

$\square$

**Problem 7.4:** Decode the received string `1101110` with the Hamming code $[7,4,1]$.

**Answer:**

$$
\left\{
\begin{array}{l}
y_1 = x_1 \oplus x_2 \oplus x_3,\\
y_2 = x_1 \oplus x_2 \oplus x_4,\\
y_3 = x_1 \oplus x_3 \oplus x_4.
\end{array} \right.
$$

* $y_1$ does not match $\Rightarrow$ the error is in one of the bits that affect $y_1$ ($y_1, x_1, x_2, x_3$).
* $y_2$ matches $\Rightarrow$ the error is in one of the bits that do not affect $y_2$ ($y_1, y_3, x_3$).
* $y_3$ matches $\Rightarrow$ the error is in one of the bits that do not affect $y_3$ ($x_2, y_1, y_2$).
* The only bit marked in all rows is $y_1$. So this is the wrong bit.

Therefore the message sent was $\mathtt{110}\textcolor{red}{\mathtt{0}}\mathtt{110}$ (and $x_1x_2x_3x_4 = \mathtt{1101}$).

An "X" in the $i$-th row of the table means that the check bit $y_i$ allows an error in the corresponding bit.

| $x_1 = \mathtt{1}$ | $x_2 = \mathtt{1}$ | $x_3 = \mathtt{0}$ | $y_1 = \mathtt{1}$ | $x_4 = \mathtt{1}$ | $y_2 = \mathtt{1}$ | $y_3 = \mathtt{0}$ |
| --- | --- | --- | --- | --- | --- | --- |
| X | X | X | X | | | |
| | | X | X | | | X |
| | X | | X | | X | |
| $\mathtt{1}$ | $\mathtt{1}$ | $\mathtt{0}$ | $\textcolor{red}{\mathtt{0}}$ | $\mathtt{1}$ | $\mathtt{1}$ | $\mathtt{0}$ |

$\square$

**Problem 7.5 (CRC by hand):** We use a "small" CRC with the generator polynomial $G(x) = x^3 + x + 1$ (bits `1011`) and a $3$-bit checksum.

* **(a)** Compute the checksum of the message `1101` -- the remainder of dividing $M(x) \cdot x^3$ by $G(x)$ modulo $2$ -- and the $7$-bit string to be transmitted.
* **(b)** Check that the receiver, dividing all $7$ bits by $G(x)$, gets the remainder $0$.
* **(c)** Show that any error that changes $1$ or $2$ of these $7$ bits will be detected. Find a $3$-bit error that this CRC does not detect.

**Answer:**

**(a)** $M(x) = x^3 + x^2 + 1$, so $M(x) \cdot x^3$ is `1101000`. We do long division, at each step adding (XOR) `1011` under the leading one:

```text
  1101000
⊕ 1011
  0110000
⊕  1011
  0011100
⊕   1011
  0001010
⊕    1011
  0000001    remainder 001
```

The checksum is `001`, and `1101` `001` = `1101001` is transmitted.

**(b)** Dividing `1101001`: the same steps as in part (a), only the last row is `0001011` $\oplus$ `1011` = `0000000`. The remainder is $0$, because $M(x) \cdot x^3 + R(x)$ is divisible by $G(x)$ (adding the remainder modulo $2$ is the same as subtracting it).

**(c)** If an error polynomial $E(x)$ is added to the transmitted polynomial $C(x)$, the receiver gets the remainder $(C + E) \bmod G = E \bmod G$. The error goes unnoticed if and only if $G(x)$ divides $E(x)$.

* In one bit: $E = x^i$. Since the constant term of $G$ is $1$, $G$ does not divide $x^i$.
* In two bits: $E = x^i (x^d + 1)$, where $1 \leq d \leq 6$. Checking $x^d \bmod G$ ($x^3 \equiv x + 1$, $x^4 \equiv x^2 + x$, $x^5 \equiv x^2 + x + 1$, $x^6 \equiv x^2 + 1$, $x^7 \equiv 1$), we see that $x^d \equiv 1$ only when $d = 7$; so in a seven-bit string $G$ does not divide $E$.
* In three bits: $E(x) = G(x) = x^3 + x + 1$ itself, or `0001011`. Adding it to `1101001` gives `1100010`, which is also divisible by $G$ -- the error goes unnoticed.

This code is a variant of the Hamming code $[7,4,1]$: its minimum distance is also $3$, so two errors can be detected (and one corrected), but three errors may go unnoticed. $\square$

**Problem 7.6 (CRC-32):** We consider the Ethernet CRC-32.

* **(a)** Show that CRC-32 detects any error burst in which all changed bits lie within at most $32$ adjacent positions.
* **(b)** Does an attacker or noise need to know the message for CRC-32 to remain unchanged? What is the minimum number of bits that must change in an Ethernet frame so that CRC-32 does not detect the change?
* **(c)** Why does checking a correct frame together with the FCS always give the same constant `0xC704DD7B`, regardless of the frame contents?

**Answer:**

**(a)** The polynomial of such an error is $E(x) = x^i \cdot B(x)$, where the degree of $B(x)$ is less than $32$ and its constant term is $1$ (the first changed bit). $G(x)$ does not divide $x^i$ (because the constant term of $G$ is $1$, it has no common factors with $x^i$) and does not divide $B(x)$ (because $B \neq 0$ and $\deg B < 32 = \deg G$). So $G$ does not divide $E$, and the error is detected.

**(b)** No. CRC-32 is an affine function: for messages of equal length $\textsf{CRC32}(m \oplus e) = \textsf{CRC32}(m) \oplus \textsf{CRC32}(e) \oplus \textsf{CRC32}(0\ldots0)$. So whether a change $e$ is detected depends only on $e$, not on the message $m$. By checking all polynomials $x^a \bmod G(x)$ up to the maximum Ethernet frame length ($1518$ bytes) with a computer, one can verify that any change of $1$, $2$ or $3$ bits is detected. But $4$ bits are enough: for example, in any $380$-byte message, flipping the bits number $0$, $140$, $791$ and $3006$ (bits are numbered from $0$, starting with the least significant bit in each byte) leaves CRC-32 unchanged. Such changes are possible only in sufficiently long frames (from about $3000$ bits), but this means that CRC-32 cannot "guarantee detecting $4$ errors" in all Ethernet frames. An attacker, in turn, can change the message at will and then adjust $32$ adjacent bits (e.g., $4$ bytes) by solving a system of linear equations modulo $2$, so that CRC-32 matches again (by part (a) this system always has a solution) -- this is why CRC does not protect against deliberate changes.

**(c)** Without the initial value and the final XOR, the register after the whole frame ($M(x) \cdot x^{32} + R(x)$) would be $0$, because it is divisible by $G(x)$. The initial value `0xFFFFFFFF` adds to the message a polynomial that depends only on the frame length; it enters both the computation of $R(x)$ and the check, so the two cancel out. Only the final XOR remains: the FCS field contains $R(x) + F(x)$, where $F(x) = x^{31} + \ldots + x + 1$ is "all ones", so the checking register ends up with

$$
F(x) \cdot x^{32} \bmod G(x) = \mathtt{0xC704DD7B},
$$

which does not depend on the message. So the "magic number" is not chosen arbitrarily -- it is the trace of the final XOR constant. Without the final XOR, checking a correct frame would give $0$. $\square$

## References

* R. Rivest, *The MD5 Message-Digest Algorithm*, [RFC 1321](https://www.rfc-editor.org/rfc/rfc1321), 1992.
* NIST, *Secure Hash Standard (SHS)*, [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final), 2015.
* R. Braden, D. Borman, C. Partridge, *Computing the Internet Checksum*, [RFC 1071](https://www.rfc-editor.org/rfc/rfc1071), 1988.
* X. Wang, H. Yu, *How to Break MD5 and Other Hash Functions*, EUROCRYPT 2005.
* M. Stevens, A. Sotirov, J. Appelbaum, A. Lenstra, D. Molnar, D. A. Osvik, B. de Weger, *Short Chosen-Prefix Collisions for MD5 and the Creation of a Rogue CA Certificate*, CRYPTO 2009.
* [Cyclic redundancy check](https://en.wikipedia.org/wiki/Cyclic_redundancy_check), [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame), [SHA-2](https://en.wikipedia.org/wiki/SHA-2).
