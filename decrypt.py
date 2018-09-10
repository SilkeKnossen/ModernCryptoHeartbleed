import collections

file_to_decode = open('cipher.txt', 'r')
# decoded_cipher_file = open('text.txt', 'w')
order = 'etaoinshrdlcumwfgypbvkjxqz'

def get_cipher():
    ch = 'a'
    cipher = []

    while ch != '\n':
        ch = file_to_decode.read(2)
        if ch != '\n':
            cipher.append(int(ch, 16))
    return cipher


def distance(v1, v2):
    v2 = vs[:len(v1)]
    return sum(abs(ord(x)-ord(y)) for x,y in zip(v1, v2))

cipher = get_cipher()
print(cipher)
