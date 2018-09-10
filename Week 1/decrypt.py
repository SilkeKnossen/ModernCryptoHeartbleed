import collections
import numpy as np
import difflib

file_to_decode = open('cipher.txt', 'r')
# decoded_cipher_file = open('text.txt', 'w')
order = 'etaoinshrdlcumwfgypbvkjxqz'

def get_cipher_text():
    ch = 'a'
    cipher = []

    while ch != '\n':
        ch = file_to_decode.read(2)
        if ch != '\n':
            cipher.append(int(ch, 16))
    return np.array(cipher)

#Get the ascii distance between two strings
def distance(v1, v2):
    v2 = v2[:len(v1)]
    return sum(abs(ord(x)-ord(y)) for x,y in zip(v1, v2))

# Sum of qi^2
def summation(distribution, pos):
    summation = 0
    total = len(distribution)
    for value in distribution.values():
        summation += (value / total)**2
    #To remove clutter, only add keys that have a non-uniform distribution
    if summation > (1/pos):
        return summation, True
    else:
        return [], False

def get_key_length_posibilities(cipher, pos):
    all_dist = []
    max_posibilites = 1.0 / pos
    #For each key length calculate the frequency
    for i in range(2, 14):
        dist = cipher[::i]
        unique, counts = np.unique(dist, return_counts=True)
        distribution = dict(zip(unique, counts))
        a, b = summation(distribution, pos)
        if b:
            all_dist += [[a, i]]
    #Get the key with the highest non uniform distribution
    all_dist = np.array(all_dist)
    all_dist = all_dist[all_dist[:,0].argsort()]

    return all_dist[::-1]

def isChar(c):
    return (c >= 32 and c < 127)

def try_all_posibilities(cipher, key_len, order):
    key = []
    for k in range(key_len): 
    # Guess each key by assuming the distrubution stays the same, even if you take each nth character
        sub_cipher = cipher[k::key_len]

        closest_key = ""
        distance_to_english = 0

        for i in range(256):  # All possible keys
            decrypt = []
            failed = False

            for character in sub_cipher: # 'decrypt all keys'
                char = character ^ i # XOR 

                if not ((char >= 44 and char <= 47) or 
                        (char >= 65 and char <= 90) or 
                        (char >= 97 and char <= 122)
                        or char == 32): # check whether or not the outcome is actually a character
                    failed = True
                    break

                char_lower = chr(char).lower()
                if char_lower >= 'a' and char_lower <= 'z':
                    decrypt += [char_lower]

            #Consider only if all characters map correctly
            if not failed: 
                #all characters map to correct output, now lets see if distribution is correct
                dist = collections.Counter(decrypt)

                freq = ''.join(x[0] for x in dist.most_common())

                ratio = difflib.SequenceMatcher(a=freq, b=order).ratio()

                if ratio >= distance_to_english:
                    distance_to_english = ratio
                    closest_key = i
        key += [closest_key]
    return key

def print_decrypt(cipher, key):
    i = 0
    output = ""
    for c in cipher:
        output += chr(c ^ key[i % len(key)])
        i += 1
    return output

cipher = get_cipher_text()
unique, counts = np.unique(cipher, return_counts=True)
distribution = dict(zip(unique, counts))
key_length = int(get_key_length_posibilities(cipher, len(distribution))[0,1])

key = try_all_posibilities(cipher, key_length, order)
output = print_decrypt(cipher, key)

print(output)
#print(key_length)
#print(cipher)
#print(order)
