import javax.crypto.Cipher;
import java.security.KeyPairGenerator;

public class LegacyAuth {
    public void oldCrypto() throws Exception {
        Cipher cipher = Cipher.getInstance("RSA/ECB/PKCS1Padding");
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(1024);
    }
    
    public void weakHash() throws Exception {
        java.security.MessageDigest md = java.security.MessageDigest.getInstance("MD5");
    }
}