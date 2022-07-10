import math

def constants():
    prime_number = [2, 3, 5, 7, 11, 13, 17, 19,
                23, 29, 31, 37, 41, 43, 47, 53,
                59, 61, 67, 71, 73, 79, 83, 89,
                97, 101, 103, 107, 109, 113, 127,
                131, 137, 139, 149, 151, 157, 163,
                167, 173, 179, 181, 191, 193, 197,
                199, 211, 223, 227, 229, 233, 239,
                241, 251, 257, 263, 269, 271, 277,
                281, 283, 293, 307, 311]
    constants = dict()
    n = 0
    s = 0
    for i in prime_number:
        s = bin(int(((i**(1/3)) - math.floor(i**(1/3))) * (2 ** 32)))[2:]
        while len(s) != 32:
            s = '0' + s
        constants[n] = s
        n += 1
    return constants

def init_hash_value():
    prime_number = [2, 3, 5, 7, 11, 13, 17, 19,
                23, 29, 31, 37, 41, 43, 47, 53,
                59, 61, 67, 71, 73, 79, 83, 89,
                97, 101, 103, 107, 109, 113, 127,
                131, 137, 139, 149, 151, 157, 163,
                167, 173, 179, 181, 191, 193, 197,
                199, 211, 223, 227, 229, 233, 239,
                241, 251, 257, 263, 269, 271, 277,
                281, 283, 293, 307, 311]
    h0 = {'a':'', 'b':'', 'c':'', 'd':'', 'e':'', 'f':'', 'g':'', 'h':''}
    cha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    square = 0
    t = 0
    for k in range(8):
        t = bin(int(((prime_number[k]**(1/2)) - math.floor(prime_number[k]**(1/2))) * (2 ** 32)))[2:]
        while len(t) != 32:
            t = '0' + t
        h0[cha[square]] = t
        square += 1
    return h0

def schedule(new_message):
    schedule = dict()
    for i in range(16):
            schedule['w{0}'.format(i)] = new_message[i * 32: i * 32 + 32]
    for j in range(16, 64):
            schedule['w{0}'.format(j)] = ADD([lower_CASE_sigma1(schedule['w{0}'.format(j-2)]), schedule['w{0}'.format(j-7)], lower_CASE_sigma0(schedule['w{0}'.format(j-15)]), schedule['w{0}'.format(j-16)]])
    return schedule
    
def compression(schedule, constants, h1):
    count = 0
    h2 = tuple(h1.values())
    while count!= 64:
        
        T1 = find_T1(schedule['w{0}'.format(count)], constants[count], h1)
        T1_T2 = ADD([T1, find_T2(h1)])
        h1['h'] = h1['g']
        h1['g'] = h1['f']
        h1['f'] = h1['e']
        h1['e'] = h1['d']
        h1['d'] = h1['c']
        h1['c'] = h1['b']
        h1['b'] = h1['a']
        h1['a'] = T1_T2
        h1['e'] = ADD([T1, h1['e']])
        count += 1
            
    h3 = {'a':ADD([h2[0], h1['a']]), 'b':ADD([h2[1], h1['b']])
         , 'c':ADD([h2[2], h1['c']]), 'd':ADD([h2[3], h1['d']])
         , 'e':ADD([h2[4], h1['e']]), 'f':ADD([h2[5], h1['f']])
         , 'g':ADD([h2[6], h1['g']]), 'h':ADD([h2[7], h1['h']])}
    
    return h3

def convert_to_hex(Block):
    code_Block1 = ''
    for e in Block.values():
        if len(bits_to_hex(e)[2:]) != 8:
            code_Block1 +=(('0' * (8-len(bits_to_hex(e)[2:]))) + bits_to_hex(e)[2:])
        else:
            code_Block1 += bits_to_hex(e)[2:]
    return code_Block1
    
def char_to_bits(ch):
    return ('0000000' + bin(ord(ch))[2:])[-8:]

def bits_to_hex( bits ):
    return hex(int(bits, 2))

def main():
    message = input('enter your messages: ')
    bit = ''
    for i in message:
        bit += char_to_bits(i)
    binary = bin(len(bit))[2:]

    bit += '1'                        # padding method ( convert to 512 bit )
    bit += '0'* (((((len(bit) // 512) + 1) * 512) - 64) - len(bit))

    while len(binary) < 64:
        binary = '0' + binary         # add length of message bit in the end
    new_message = bit + binary
    
    for i in range(len(new_message)//512):
        if i == 0:
            h3 = compression(schedule(new_message[:512]), constants(), init_hash_value())
        elif i > 0:
            h3 = compression(schedule(new_message[512 * i:512 * (i+1)]), constants(), h3)

    print(convert_to_hex(h3))

    
#--------------------------------------------------------
def SHR(k, x):
    if k <= len(str(x)):
        b = ('0' * k) + str(x)[:len(str(x)) - k]
    else:
        b = '0' * len(str(x))
    return b

def ROTR(n, x):
    while n >= len(str(x)):
        n = n % len(str(x))
    c = str(x)[len(str(x)) - n:len(str(x))] + str(x)[:len(str(x)) - n]
    return c
    
def XOR(l): # l is a list of bit
    n = 0
    a = 0
    result = ''
    for i in range(len(l[0])):
        while n < len(l):
            a = abs(int(l[n][i]) - a)
            n += 1
        result += str(a)
        a = 0
        n = 0
    return result

def ADD(r): # r is a list of bit
    a = 0
    for i in r:
        a += int(i, 2)
    result = bin(a % (2 ** 32))[2:]
    while len(result) != 32:
        result = '0' + result
    return result

#---------------------------------------------------------

def lower_CASE_sigma0(x):
    return XOR([ROTR(7, x), ROTR(18, x), SHR(3, x)])

def lower_CASE_sigma1(x):
    return XOR([ROTR(17, x), ROTR(19, x), SHR(10, x)])

def upper_CASE_sigma0(x):
    return XOR([ROTR(2, x), ROTR(13, x), ROTR(22, x)])

def upper_CASE_sigma1(x):
    return XOR([ROTR(6, x), ROTR(11, x), ROTR(25, x)])
    
def COOR(x, y, z):
    result = ''
    for i in range(len(x)):
        if x[i] == '0':
            result += z[i]
        elif x[i] == '1':
            result += y[i]
    return result

def MAJOR(x, y, z):
    result = ''
    for i in range(len(x)):
        if x[i] == y[i] or x[i] == z[i]:
            result += x[i]
        else:
            result += y[i]
    return result

def find_T1(w, constant, h0):
    return ADD([upper_CASE_sigma1(h0['e']), COOR(h0['e'], h0['f'], h0['g']), h0['h'], constant, w])

def find_T2(h0):
    return ADD([upper_CASE_sigma0(h0['a']), MAJOR(h0['a'], h0['b'], h0['c'])])
#--------------------------------------------------------
main()
    
   





            
