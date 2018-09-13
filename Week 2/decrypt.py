import collections
import numpy as np
import difflib

file_to_decode = open('cipher.txt', 'r')
# decoded_cipher_file = open('text.txt', 'w')
order = 'etaoinshrdlcumwfgypbvkjxqz'

known = np.zeros((7, 31))
# known[sentence][character] = letter it should be

known[0][0]  = ord("I")
known[0][1]  = ord(" ")
known[0][2]  = ord("a")
known[0][3]  = ord("m")
known[0][4]  = ord(" ")
known[1][5]  = ord(" ")
known[4][6]  = ord("k")
known[4][7]  = ord(" ")
known[1][8]  = ord("e")
known[2][10] = ord("t")
known[2][11] = ord(" ")
known[0][12] = ord("g")
known[0][13] = ord(" ")
known[1][14] = ord(" ")
known[2][15] = ord("n")
known[2][17] = ord("i")
known[1][20] = ord("n")
known[1][21] = ord(" ")
known[6][23] = ord(" ")
known[0][24] = ord("i")
known[0][25] = ord("s")
known[0][26] = ord("s")
known[0][27] = ord("i")
known[0][28] = ord("o")
known[0][29] = ord("n")
known[0][30] = ord(".")



def get_cipher_text():
    ch = 'a'
    cipher = []

    while ch != '|':
        ch = file_to_decode.read(1)
        if ch == '\n' or ch == '|':
            continue
        ch += file_to_decode.read(1)
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

def try_all_posibilities(cipher, key_len, order, known):
    key = []
    for k in range(key_len): 
    # Guess each key by assuming the distrubution stays the same, even if you take each nth character
        sub_cipher = cipher[k::key_len]

        closest_key = ""
        distance_to_english = 0


        for i in range(256):  # All possible keys
            decrypt = []
            failed = False

            for character in range(len(sub_cipher)): # 'decrypt all keys'
                char = sub_cipher[character] ^ i # XOR 

                sen = int((character * key_len + k) / 31)
                let = int((character * key_len + k) % 31)

                # check whether or not the outcome is actually a character
                if not ((char == 46) or 
                        (char >= 65 and char <= 90) or 
                        (char >= 97 and char <= 122) or
                        (char >= 32 and char <= 32) or
                        char == 63): 
                    failed = True
                    break

                #Now lets check where it should map to and if it does
                if known[sen][let] and char != known[sen][let]:
                    #print(known[sen][let])
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
    for c in cipher:
        if i % 31 == 0:
            print("\n", end="")
        print(chr(c ^ key[i % len(key)]), end="")
        i += 1

cipher = get_cipher_text()
unique, counts = np.unique(cipher, return_counts=True)
distribution = dict(zip(unique, counts))
#key_length = int(get_key_length_posibilities(cipher, len(distribution))[0,1])
key_length = 31
key = try_all_posibilities(cipher, key_length, order, known)
print_decrypt(cipher, key)


