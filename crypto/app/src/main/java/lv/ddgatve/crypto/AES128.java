package lv.ddgatve.crypto;

import java.security.GeneralSecurityException;
import java.security.Security;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

import org.bouncycastle.jce.provider.BouncyCastleProvider;

/** 
 * Reference AES document: 
 * https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf
 */

public class AES128 {

    static {
        // In fact, should add provider to java.security. 
        // This line seems useless
        Security.addProvider(new BouncyCastleProvider());
    }

    public static byte[] ecbEncrypt(SecretKey key, byte[] data)
            throws GeneralSecurityException {
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS7Padding", "BC");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data);
    }

    public static byte[] ecbDecrypt(SecretKey key, byte[] cipherText)
            throws GeneralSecurityException {
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS7Padding", "BC");
        cipher.init(Cipher.DECRYPT_MODE, key);
        return cipher.doFinal(cipherText);
    }

    public static SecretKey defineKey(byte[] keyBytes) {
        if (keyBytes.length != 16 && keyBytes.length != 24 && keyBytes.length != 32) {
            throw new IllegalArgumentException("keyBytes wrong length for AES key");
        }
        return new SecretKeySpec(keyBytes, "AES");
    }

    public static void main(String[] args) {
        //Setup.installProvider();
        String javaHome = System.getProperty("java.home");
        System.out.println("JAVA_HOME = " + javaHome);


        // This is from AES standard
        // String sBlockHex = "00112233445566778899aabbccddeeff";
        // String sKeyHex = "000102030405060708090a0b0c0d0e0f";
        // String sOutputHex = "69c4e0d86a7b0430d8cdb78070b4c55a";

        String sBlockHex = "48656c6c6f20776f726c642120202020";
        String sKeyHex = "def4be2036b28d9cc8e4388452635414";
        String sOutputHex = "e80027fcb3f4107706845341cc1d371c";

        byte[] keyBytes = Utils.x2a(sKeyHex);
        SecretKey secretKey = defineKey(keyBytes);
        byte[] blockBytes = Utils.x2a(sBlockHex);

        try {    
            byte[] cipherText = ecbEncrypt(secretKey, blockBytes);
            System.out.println("cipherText length is " + cipherText.length);
            String result = Utils.a2x(cipherText, 0, cipherText.length);
            System.out.println("result = " + result);
            System.out.println("expect = " + sOutputHex);
        } 
        catch (GeneralSecurityException e) {
            System.out.println(e.getMessage());
        }
    }
}