#include <openssl/des.h>
#include <openssl/rsa.h>
#include <openssl/md5.h>

void old_crypto() {
    DES_cblock key;
    DES_key_schedule schedule;
    DES_set_key(&key, &schedule);
    
    RSA *rsa = RSA_generate_key(1024, 65537, NULL, NULL);
    
    MD5_CTX ctx;
    MD5_Init(&ctx);
}