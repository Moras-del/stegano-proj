from steganos import *
import sys
def readBitsFromFile(path):
    bits = ''
    with open(path, 'r') as file:
        for byte in file.read():
            bits += bin(int('0x' + byte, 16))[2:].zfill(4)
    return bits

def createEncodingStegano(opt):
    if opt == 1:
        return SpaceLineEncoder('file.html')
    elif opt == 2:
        return SpaceEncoder('file.html')

def createDecodingStegano(opt):
    if opt == 1:
        return SpaceLineDecoder('watermark.html')
    elif opt == 2:
        return SpaceDecoder('watermark.html')

def encrypt(steganoOpt):
    stegano = createEncodingStegano(steganoOpt)
    bits = readBitsFromFile('mess.txt')
    stegano.encode('watermark.html', bits)

def decrypt(steganoOpt):
    stegano = createDecodingStegano(steganoOpt)
    data = stegano.decode()
    with open('detect.txt', 'w') as file:
        file.write(data)

if __name__ == '__main__':

    opt = sys.argv[1]
    print('Wybierz algorytm: ')
    print('1) spacja na koniec wiersza')
    print('2) podwójne spacje')
    stegano = int(input())
    if opt == '-e':
        encrypt(stegano)
    elif opt == '-d':
        decrypt(stegano)
