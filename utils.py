def getGenDescriptions(filename):
    text = readFile(filename)
    return getGens(text)


# Reads the file - Only full paths
def readFile(fileName):
    test = open(fileName)
    text = [line.rstrip('\n') for line in open(fileName, 'r')]
    return text

def getGens(text):
    arrayGens = []
    for t in text:
        temp = getGen(t)
        arrayGens.append(temp)
    print(arrayGens)

    return arrayGens

def getGen(string):
    flag = False
    value = ""
    for s in string:
        if s == "-":
            flag = True
        elif flag:
            # if not s == " ":/
            value +=s
    return value