luaFile = open("recipe.lua", "r")

# read lines and delete last and first line
luaFile.readline()
linesLua = luaFile.readlines()
linesLua.pop()
luaFile.close()

textLua = "".join(linesLua)
tokens = []

token = ""
specialChars = {'{', '}', ','}

def addToken(token):
    if token != "":
        if token[-1] != '"' and token != "true" and token != "false" and not token[0].isnumeric():
            token = f'"{token}"'
        tokens.append(token)
    token = ""

for char in textLua:
    if token == "--":
        if char == '\n':
            token = ""
    elif char == '=':
        addToken(token)
        token = ""
        tokens.append(':')
    elif char in specialChars:
        addToken(token)
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

# dump data to json file
jsonFile = open("data/recipe.json", "w+")
jsonFile.writelines(textJson)
jsonFile.close()