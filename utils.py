def getGenDescriptions(filename):
    text = readFile(filename)
    return getGens(text)


# Reads the file - Only full paths
def readFile(fileName):
    test = open(fileName)
    text = [line.rstrip('\n') for line in open(fileName, 'r')]
    return text

def getGens(text):
    hashGens = {}
    for t in text:
        temp = getPair(t)
        hashGens.update(temp)
    print(hashGens)

    return hashGens

def getPair(string):
    key = ""
    value = ""
    flag = False
    for s in string:
        if s == ":":
            flag = True
        elif flag:
            if not s == " ":
                value +=s
        else:
            key+=s
    return {key: value}