from math import ceil, sqrt
import random, base64

def is_prime(n) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, ceil(sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_relative_prime(a, b) -> bool:
    while b:
        a, b = b, a % b
    return a == 1

def find_mod_inverse(a, m) -> int:
    return pow(a, -1, m)

def generate_random_prime() -> int:
    while True:
        n = random.randint(100, 1000)
        if is_prime(n):
            return n
        
def is_relative_prime(a, b) -> bool:
    while b:
        a, b = b, a % b
    return a == 1

def generate_public_key() -> tuple[int, int]:
    e = 65537 # 2^16 + 1, a common choice for RSA encryption
    while True:
        p = generate_random_prime()
        q = generate_random_prime()
        n = p * q
        totient_n = (p - 1) * (q - 1)
        if is_relative_prime(totient_n, e):
            break
    return e, n

def generate_private_key() -> tuple[int, int]:
    p = generate_random_prime()
    q = generate_random_prime()
    e = 65537 # 2^16 + 1, a common choice for RSA encryption
    n = p * q
    totient_n = (p - 1) * (q - 1)
    d = find_mod_inverse(e, totient_n)
    return d, n

def convert_message_to_int(message: str) -> int:
    array = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    temp = ""
    for char in message:
        index = array.index(char)
        if index < 10:
            temp = temp + "0" + str(index)
        else:
            temp = temp + str(index)
    return int(temp)

def convert_int_to_message(number: int) -> str:
    array = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    number = str(number)
    message = ""
    for i in range(0, len(number), 2):
        index = int(number[i:i+2])
        message += array[index]
    return message

def encrypt(plaintext, e, n) -> str:
    # convert the plaintext to an integer
    plaintext = str(convert_message_to_int(plaintext))

    # split the plaintext into blocks of 4 digits
    blocks = [plaintext[i:i+4] for i in range(0, len(plaintext), 4)]
    
    # encrypt each block
    ciphertext = []
    for block in blocks:
        ciphertext.append(pow(int(block), e, n))

    return ciphertext

def decrypt(ciphertext, d, n) -> str:
    # decrypt each element of the ciphertext
    blocks = []
    for i in range(len(ciphertext)):
        blocks.append(pow(ciphertext[i], d, n))
    print('blocks:', blocks)

    # convert each element of blocks to string
    plaintext = "".join([str(block).zfill(4) for block in blocks])
    result = convert_int_to_message(int(plaintext))
    return result

# e, n = generate_public_key()
# d, n = generate_private_key()    
# plaintext = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
# b64 = str(base64.b64encode(plaintext.encode('utf-8')).decode('utf-8'))
# print('b64:', b64)
# print('to int:', convert_message_to_int(b64))
# ciphertext = encrypt(b64, e, n)
# print('ciphertext:', ciphertext)
# plaintext = decrypt(ciphertext, d, n)
# print(plaintext)