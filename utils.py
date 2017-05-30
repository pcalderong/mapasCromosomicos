def getGenDescriptions(filename):
    text = readFile(filename)
    return getGens(text)

def saveFile(gens, probaility, count):
    file = open("files/recombinationFile" + str(count) + ".txt", "w")
    file.write("Gens\n")
    file.write("====\n")
    i = 0
    for g in gens:
        file.write("GE"+str(i)+" = " + g.get_text() + "\n")
        i += 1
    file.write("Probability\n")
    file.write("===========\n")
    i = 0
    j = 0
    for p in probaility:
        for col in p:
            if i>j:
                file.write("GE"+str(j)+" - GE"+str(i)+" = "+col.get_text()+"\n")
            i += 1
        j += 1
        i =0
    file.close()

# Reads the file - Only full paths
def readFile(fileName):
    test = open(fileName)
    text = [line.rstrip('\n') for line in open(fileName, 'r')]
    return text

def readFileWithProb(fileName):
    test = open(fileName)
    listGens = []
    matrixProb = []
    text = [line.rstrip('\n') for line in open(fileName, 'r')]
    flagGen = False
    flagProb = False
    for i in text:
        if (i == "Gens"):
            flagGen = True
        elif (i == "Probability"):
            flagGen = False
            flagProb = True
            print(listGens)
            matrixProb = generateMatrix(len(listGens))
        elif flagGen and not("===" in i):
            line = i.rsplit(" = ")
            listGens.append(line[1])
        elif flagProb and not("===" in i):
            line = i.rsplit(" = ")
            index = line[0].rsplit(" - ")
            i = int(index[0][2:])
            j = int(index[1][2:])
            matrixProb[i][j] = line[1]
    return [listGens, matrixProb]

def generateMatrix(size):
    matrix = []
    for i in range(0,size):
        row = []
        for j in range(0,size):
            if i <= j:
                row.append("0.0")
            else:
                row.append("---")
        matrix.append(row)
    return matrix

def getGens(text):
    arrayGens = []
    for t in text:
        temp = getGen(t)
        arrayGens.append(temp)
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

class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3