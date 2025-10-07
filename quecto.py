class Femto:
    def __init__(self):
        self.text = ['']
        self.textpath = ''
    def read(self, textpath):
        self.text = ['']
        self.textpath = textpath
        try:
            with open(textpath, 'r') as file:
                self.text = file.readlines()
        except:
            pass
    def write(self, line, content):
        if line < len(self.text):
            self.text[line] = content + '\n'
    def save(self):
        self.text = [line.replace('\t', '    ') for line in self.text]
        with open(self.textpath, 'w') as file:
            file.writelines(self.text)
    def printline(self, line):
        if line < len(self.text):
            pline = self.text[line].replace('\n', '')
            print(f"{line}: {pline}")
    def printall(self):
        for i in range(len(self.text)):
            cleanline = self.text[i].replace('\n', '')
            print(f'{i}: {cleanline}')
    def search(self, line, substring):
        if line < len(self.text):
            replaced = self.text[line].replace(substring, f"[{substring}]").replace('\n', '')
            print(f'{line}: {replaced}')
    def searchall(self, substring):
        for i, line in enumerate(self.text):
            if substring in line:
                replaced = line.replace(substring, f"[{substring}]").replace('\n', '')
                print(f'{i}: {replaced}')
    def replace(self, line, old, new):
        if line < len(self.text):
            self.text[line] = self.text[line].replace(old, new)
    def replaceall(self, old, new):
        for i in range(len(self.text)):
            self.text[i] = self.text[i].replace(old, new)
    def delete(self, line):
        if line < len(self.text):
            del self.text[line]
    def clear(self):
        self.text = ['']
quecto = Femto()
path = ''
index = 0
edit = False
running = True
while running:
    command = input(f'<{path}[{index}]>:')
    parts = command.split(' ')
    if parts[0] == ':exit':
        running = False
    elif parts[0] == ':open':
        if len(parts) > 1:
            path = parts[1]
            quecto.read(path)
            index = 0
            path = path.split('/')[-1]
    elif parts[0] == ':edit':
        previndex = index
        if len(parts) > 1 and parts[1].isdigit():
            newindex = int(parts[1])
            if 0 <= newindex < len(quecto.text):
                index = newindex
                edit = True
    elif parts[0] == ':goto':
        if len(parts) > 1 and parts[1].isdigit():
            newindex = int(parts[1])
            if 0 <= newindex < len(quecto.text):
                index = newindex
    elif parts[0] == ':save':
        if len(parts) > 1:
            quecto.textpath = parts[1]
            path = parts[1].split('/')[-1]
        quecto.save()
    elif parts[0] == ':print':
        if len(parts) > 1:
            if parts[1] == 'all':
                quecto.printall()
            elif parts[1].isdigit():
                num = int(parts[1])
                if 0 <= num < len(quecto.text):
                    quecto.printline(num)
        else:
            quecto.printline(index)
    elif parts[0] == ':search':
        if len(parts) > 2:
            if parts[1] == 'all':
                quecto.searchall(parts[2])
            elif parts[1].isdigit():
                linenum = int(parts[1])
                if 0 <= linenum < len(quecto.text):
                    quecto.search(linenum, parts[2])
        elif len(parts) > 1:
            quecto.search(index, parts[1])
    elif parts[0] == ':replace':
        if len(parts) > 3:
            if parts[1] == 'all':
                quecto.replaceall(parts[2], parts[3])
            elif parts[1].isdigit():
                linenum = int(parts[1])
                if 0 <= linenum < len(quecto.text):
                    quecto.replace(linenum, parts[2], parts[3])
        elif len(parts) > 2:
            quecto.replace(index, parts[1], parts[2])
    elif parts[0] == ':delete':
        if len(parts) > 1:
            if parts[1] == 'all':
                quecto.clear()
                index = 0
            elif parts[1].isdigit():
                deline = int(parts[1])
                if 0 <= deline < len(quecto.text):
                    quecto.delete(deline)
                    if index > deline:
                        index -= 1
                    elif index == deline:
                        index = min(index, len(quecto.text) - 1)
                    if index < 0:
                        index = 0
        else:
            quecto.delete(index)
            if index >= len(quecto.text):
                index = max(0, len(quecto.text) - 1)
    elif parts[0] == ':head':
        index = 0
    elif parts[0] == ':tail':
        index = len(quecto.text) - 1 if quecto.text else 0
    else:
        if not command.startswith(':'):
            quecto.write(index, command)
            if edit:
                edit = False
                index = previndex
            else:
                if index == len(quecto.text) - 1:
                    quecto.text.append('')
                index += 1