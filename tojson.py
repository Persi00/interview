def readDataFile(path : str) -> list:
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    return lines

def dumpJsonFile(path : str, textJson : str):
    jsonFile = open(path, "w+")
    jsonFile.writelines(textJson)
    jsonFile.close()

def addToken(token, tokens):
    if token != "":
        if token[-1] != '"' and token != "true" and token != "false" and not token[0].isnumeric():
            token = f'"{token}"'
        tokens.append(token)
    token = ""

def ToJson(linesData : list) -> str:
    linesData.pop()
    linesData.pop(0)
    textData = "".join(linesData)
    tokens : list = []

    token = ""
    specialChars = {'{', '}', ','}

    for char in textData:
        if token == "--":
            if char == '\n':
                token = ""
        elif char == '=':
            addToken(token, tokens)
            token = ""
            tokens.append(':')
        elif char in specialChars:
            addToken(token, tokens)
            token = ""
            tokens.append(char)
        elif char != ' ' and char != '\n':
            token += char

    leftBracketsStack = []

    for i in range(len(tokens)):
        if tokens[i] == '{':
            tokens[i] = '['
            leftBracketsStack.append(i)
        elif tokens[i] == ':' and tokens[leftBracketsStack[-1]] == '[':
            tokens[leftBracketsStack[-1]] = '{'
        elif tokens[i] == '}':
            if tokens[leftBracketsStack[-1]] == '[':
                tokens[i] = ']'
            leftBracketsStack.pop()


    textJson = f'{"".join(tokens)}'.replace(',}', '}').replace(',]', ']')
    return textJson

if __name__ == "__main__":
    linesData = readDataFile("data/recipe.lua")
    textJson = ToJson(linesData)
    dumpJsonFile("data/recipe.json", textJson)