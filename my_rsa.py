# rsa like encryption algorithm



import random
import math as m

# Checking if the number is prime or not
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(m.sqrt(number))+1):
        if number % i == 0:
            return False
    return True


# For generating a prime number between two given numbers
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# For generating a private key from the public key
def mod_inverse(p_key, phi):
    for s_key in range(3, phi):
        if (s_key * p_key) % phi == 1:
            return s_key
    raise ValueError("Mod inverse doesn't exist")

# Function to genetate public and private key pair
def newkeys():
    '''
    Generate Public and Private keys and return them in the format (pub, priv) 
    '''
    
    p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q
    phi_n = (p-1) * (q-1)    # Calculating the vlaue of the Euler's Totient function

    p_key = random.randint(3, phi_n -1)
    while m.gcd(p_key, phi_n) != 1:
        p_key = random.randint(3, phi_n -1)   # Generating the public key

    s_key = mod_inverse(p_key, phi_n)    # Generating the private key

    return (n, p_key), (n, s_key)


def encrypt(message, key):
    '''
    args: message --> str, key --> tuple
    returns cipher --> str
    '''

    n, p_key = key
    encoded_message = [ord(ch) for ch in message]   # Converting each character to its ascii code

    # c = (m ^ e) mod phi(n) --> cipher number of each ascii code number
    ciphertext = [pow(ch, p_key, n) for ch in encoded_message]
    ciphertext = str(ciphertext)  # Converting the list into a string

    return ciphertext

def decrypt(ciphertext, key):
    '''
    args: ciphertest --> str, key --> tuple
    returns message --> str
    '''

    ciphertext = eval(ciphertext)  # Converting the string into a list of integers
    n, s_key = key

    # m = (c ^ d) mod phi(n) --> deciphering the ciphered numbers of each ascii code number
    deciphertext = [pow(ch, s_key, n) for ch in ciphertext]

    decoded_message = "".join(chr(ch) for ch in deciphertext)  # Converting the respective ascii to it's character and joined them

    return decoded_message

# To send the public key in clean text format
def save_pkcs1(key):
    '''
    args: key --> tuple
    saves key in str format
    '''

    n, exp = key
    return f"-----BEGIN RSA PUBLIC KEY-----\n{n}\n{exp}\n-----END RSA PUBLIC KEY-----"
    
# To receive the public key and convert it to numbers
def load_pkcs1(str):
    '''
    args: key in the form of text
    returns key --> tuple
    '''

    lines = str.split("\n")
    n = int(lines[1])
    exp = int(lines[2])

    return n, exp