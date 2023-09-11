import sys
from hashlib import sha256

n = 0xda52c9a04a7ae06ce0be31fd3c49a3e8d7c1466731db176de26b2462015e87a28d8b3cb564a9f4fc2b859dcb94b1500b2f8b375043400fe6a4852237a1fc4563a6d2b4e3889b73cddcd4d5da3150ab1f3ebc896c7e8dd7b286df0134d4c3960803d5d69e509771e33d95462f7c765d78656f945e51a0e1fcbe6dfaddba415a5ce39df27d617c5c7024cb3b4748c05dc7a2bc278dd6d6bb8b74472c45e2504b7c26a8b90935f3a3abbeef6da5423473cd718cdd769060fd1ab7952c68b2211a792940c0a1a3820c63db2d081cc4286a4baa28fca9f0691f7906e69eb1e5be8221b1ab0b66883f47196d0e72295f784eb0debe6441ad8b458025f6eb89489cedf3

pow1 = 0x678c3c0c4d9fcca4e03c1610a85c96fb95eba016dec44af97689f9d425897a4031909ccf80b000ac2ec3099345bfd10d17309c4a48a8ce17adbb812cf8490066c46d274899f174111ee174870e31e591764926da008f1f359010185a2ed9fc57965b1b800cd1242768f7c1568bb8fd90364a0ebc569c35d302e6ad70bbf958ac93e62de38c2d8e1ee0c11dc630261d42671ec2bde7f6a6d19957ed61879ece80a36e8ef2f5c534f5872020e3119635f52b8089c057d787e2fb5c49c2ca11f3566c22d553b319f6867d40446c5b8c6c95ee70747db23b4113d916f2e13d9835aeffe3dc8b47b903385e4315856ea75a991a1f41ac1762a443e5f4aa4c36cd3f46
pow2 = 0xeae6a3ed0c4eb7d8b6c7ee0c5294a317730f15d5236efd896ac1c802267a5f1e43a79e8109cd10ea8e9c0fc869c2d358afc1e04299069acaff6821349d00e9566e2e2748b7740ddd12c0b64a1136916198f1e747bccdae0b748b83d2929c3d6babc5c033ac4e82b968c4ff4183ca247fad3217b284f6b92fd60479d032d78fb13f2149e66665eef5bb6be0bc33cd1addc4fe27b4a553167e19f398ec1357ab2df8b6d3bcbff7efc3986bac68a55462b44f15cf2d7282a926e4e634a4da4bbe8e8db83aad9992b565742cc4fb8b57adc1e72db33ed052cb56272cb2f9f6091ae5058c60fe030c568f16356cb9e6cdecf8f386861905b4a0e212d1fcb2a7969415

def inv(a, n):
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return 0
    if t < 0:
        t = t + n
    return t

def rsa(c, n):
    a = pow(c, pow1, n)
    b = pow(c, pow2, n)
    i = inv(b, n)
    return a*i % n

i_hex = sys.argv[1]
i_int = int(i_hex, 16)
o_int = rsa(i_int, n)
o_bin = o_int.to_bytes(256, 'big', signed = False)
hash = sha256()
hash.update(o_bin)
print(hash.digest().hex(), end='')
