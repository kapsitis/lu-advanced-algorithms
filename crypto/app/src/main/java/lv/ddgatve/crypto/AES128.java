package lv.ddgatve.crypto;

import java.security.GeneralSecurityException;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class AES128 {

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


        String sBlockHex = "00112233445566778899aabbccddeeff";
        String sKeyHex = "000102030405060708090a0b0c0d0e0f";
        String sOutputHex = "69c4e0d86a7b0430d8cdb78070b4c55a";

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