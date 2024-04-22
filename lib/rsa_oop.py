import random
from math import ceil, sqrt

class RSA:
    def __init__(self):
        self.p = None
        self.q = None
        self.e = 65537 # 2^16 + 1, a common choice for RSA encryption
        self.d = None
        self.n = None
        self.public_key = None
        self.private_key = None

    def is_prime(self, n):
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

    def generate_random_prime(self):
        while True:
            n = random.randint(pow(1024-1, 2), pow(1024, 2))
            if self.is_prime(n):
                return n

    def is_relative_prime(self, a, b):
        while b:
            a, b = b, a % b
        return a == 1

    def find_mod_inverse(self, a, m):
        return pow(a, -1, m)

    def generate_keys(self):
        while True:
            self.p = self.generate_random_prime()
            self.q = self.generate_random_prime()
            self.n = self.p * self.q
            totient_n = (self.p - 1) * (self.q - 1)
            if self.is_relative_prime(totient_n, self.e):
                break
        
        self.d = self.find_mod_inverse(self.e, totient_n)
        self.public_key = (self.e, self.n)
        self.private_key = (self.d, self.n)

    def convert_message_to_int(self, message):
        array = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        temp = ""
        for char in message:
            index = array.index(char)
            if index < 10:
                temp = temp + "0" + str(index)
            else:
                temp = temp + str(index)
        return int(temp)
    
    def convert_int_to_message(self, number):
        array = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        number = str(number)
        message = ""
        for i in range(0, len(number), 2):
            index = int(number[i:i+2])
            message += array[index]
        return message

    def encrypt(self, plaintext):
        # plaintext is converted to base64 already
        # convert base64 to int indexing
        plaintext = str(self.convert_message_to_int(plaintext))

        # split the plaintext into blocks of 4 digits
        blocks = [plaintext[i:i+4] for i in range(0, len(plaintext), 4)]

        # encrypt each block
        ciphertext = []
        for block in blocks:
            ciphertext.append(pow(int(block), self.e, self.n))

        return ciphertext

    def decrypt(self, ciphertext):
        # ciphertext is in int form
        # decrypt each element of the ciphertext
        blocks = []
        for i in range(len(ciphertext)):
            blocks.append(pow(ciphertext[i], self.d, self.n))
        
        # convert each element of blocks to string
        plaintext = "".join([str(block).zfill(4) for block in blocks])
        result = self.convert_int_to_message(int(plaintext))
        return result