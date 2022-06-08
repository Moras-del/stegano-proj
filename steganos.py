class SteganoEncoder:

    def __init__(self, path):
        with open(path, 'r') as file:
            self.html = file.readlines()

    def encode(self, path, data):
        with open(path, 'w') as file:
            if self._checkLen(len(data)):
                print('Za duża wiadomość dla podanej opcji!')
                return
            self.writeDataLen(file, data)
            self._encodeImpl(file, data)

    def _encodeImpl(self, file, data):
        pass

    def writeDataLen(self, file, data):
        file.write(f'<!--{len(data)}-->\n')


class SteganoDecoder:

    def __init__(self, path):
        with open(path, 'r') as file:
            self.html = file.readlines()

    def readDataLen(self):
        return int(self.html[0][4:-4])

    def decode(self):
        n = self.readDataLen()
        return self._decodeImpl(n)

    def _decodeImpl(self, n):
        pass


# 1)
class SpaceLineEncoder(SteganoEncoder):

    def _checkLen(self, n):
        return n > len(self.html)

    def _encodeImpl(self, file, data):
        for index, line in enumerate(self.html):
            if line.endswith(' \n'):
                line = line[:-2]
            if (index < len(data)):
                if data[index] == '1':
                    line = line[:-1]
                    line += ' \n'
            file.write(line)


class SpaceLineDecoder(SteganoDecoder):
    def _decodeImpl(self, n):
        result = ''
        curr = ''
        for index, line in enumerate(self.html[1:]):
            if index >= n:
                break
            if line.endswith(' \n'):
                curr += '1'
            else:
                curr += '0'
            if len(curr) == 4:
                result += hex(int(curr, 2))[-1]
                curr = ''
        return result


# 2)
class SpaceEncoder(SteganoEncoder):

    def _checkLen(self, n):
        count = 0
        for line in self.html:
            if line.startswith('  ') or line.startswith('    ') or line.startswith('\t'):
                continue
            line.replace('  ', ' ')
            for char in line:
                if char == ' ':
                    count += 1
        return n > count

    def _encodeImpl(self, file, data):
        counter = 0
        omitNext = False
        for line in self.html:
            currLine = line
            if 'azureedge' in line:
                v = 3
            start = 0
            if line.startswith('  '):
                start = 2
            if line.startswith('    '):
                start = 4
            for i in range(start, len(line)):
                if counter == len(data):
                    break
                if omitNext:
                    omitNext = False
                    continue
                if currLine[i] == ' ':
                    if data[counter] == '0':
                        counter += 1
                    else:
                        currLine = currLine[:i] + ' ' + currLine[i:]
                        omitNext = True
                        counter += 1
            file.write(currLine)

class SpaceDecoder(SteganoDecoder):
    def _decodeImpl(self, n):
        result = ''
        curr = ''
        omitNext = False
        for line in self.html[1:]:
            start = 0
            if line.startswith('  '):
                start = 2
            if line.startswith('    '):
                start = 4
            for i in range(start, len(line)-1):
                if omitNext:
                    omitNext = False
                    continue
                if len(result)*4 >= n:
                    return result
                if line[i] == ' ':
                    curr += '1' if line[i+1] == ' ' else '0'
                    omitNext = True
                    if len(curr) == 4:
                        result += hex(int(curr, 2))[-1]
                        curr = ''

class MarkerEncoder(SteganoEncoder):
    def _checkLen(self, n):
        count = 0
        for line in self.html:
            count += line.count('<p>')
            count += line.count('</p>')
        return n > count

    def _encodeImpl(self, file, data):
        lineIndex = 0
        for bit in data:
            found = False
            while not found:
                line = self.html[lineIndex]
                marker = '<p>' if bit == '1' else '</p>'
                if marker in line:
                    if bit == '1':
                        pass

