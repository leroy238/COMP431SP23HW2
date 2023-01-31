#Justin Smith, COMP 431

import string
import sys

curr_message = ""
full_message = ""
addresses = []

def printError500():
    print("500 Syntax error: command unrecognized")

def printError501():
    print("501 Syntax error in parameters or arguments")

def printError503():
    print("503 Bad sequence of commands")

def print250():
    print("250 OK")

def print354():
    print("354 Start mail input; end with <CRLF>.<CRLF>")

def messageToFile(mailAddress):
    file = None
    try:
        file = open("forward/" + mailAddress, "a")
    except Exception:
        file = open("forward/" + mailAddress, "x")
    finally:
        file.write(full_message[:len(full_message)-1])
        file.close()

def isSpace(index):
    if curr_message[index] == '\t' or curr_message[index] == ' ':
        return True
    return False

def isLetter(index):
    if string.ascii_letters.find(curr_message[index]) != -1:
        return True
    return False

def isDigit(index):
    if string.digits.find(curr_message[index]) != -1:
        return True
    return False

def isNull(index):
    return True

def isSpecial(index):
    special_chars = r'<>()[]\.,:@"';
    if special_chars.find(curr_message[index]) != -1:
        return True
    return False

def isCRLF(index):
    if curr_message[index] == '\n':
        return True
    return False

def isChar(index):
    if string.printable.find(curr_message[index]) != -1 and not(isSpecial(index) or isSpace(index)):
        return True
    return False

def isLetterDigit(index):
    if isLetter(index) or isDigit(index):
        return True
    return False

def whitespace(index):
    if index >= len(curr_message):
        return -1
    if isSpace(index):
        index += 1
        return whitespace(index)
    return index

def isNullspace(index):
    if index >= len(curr_message):
        return index
    if isSpace(index):
        index += 1
        return whitespace(index)
    if isNull(index):
        return index
    return -1

def letDigStr(index):
    if index >= len(curr_message):
        return -1
    if isLetterDigit(index):
        index += 1
        return letDigStr(index)
    return index

def name(index):
    if isLetter(index):
        index += 1
        letDigIndex = letDigStr(index)
        if letDigIndex > index:
            return letDigIndex
    #else:
    #    printError501()
    return -1

def element(index):
    letterIndex = index
    if isLetter(index):
        letterIndex += 1

    if letterIndex == index:
        #printError501()
        return -1

    nameIndex = name(index)
    
    if nameIndex > letterIndex:
        return nameIndex
    else:
        return letterIndex

def domain(index):
    elementIndex = element(index);
    if elementIndex > index:
        if elementIndex < len(curr_message) and curr_message[elementIndex] == '.':
            domainIndex = domain(elementIndex + 1)
            if domainIndex > elementIndex + 1:
                return domainIndex
            else:
                return -1
        return elementIndex
    return -1

def indexString(index):
    if index >= len(curr_message):
        return -1
    if isChar(index):
        index += 1
        return indexString(index)
    return index

def localPart(index):
    stringIndex = indexString(index)
    if stringIndex > index:
        return stringIndex
    #else:
        #printError501()
    return -1

def mailbox(index):
    localIndex = localPart(index)
    if localIndex > index:
        if localIndex < len(curr_message) and curr_message[localIndex] == '@':
            domainIndex = domain(localIndex + 1)
            if domainIndex > localIndex + 1:
                return domainIndex
            else:
                return -1
        #else:
            #printError501()
    return -1

def path(index):
    if curr_message[index] == '<':
        index += 1
        mailIndex = mailbox(index)
        if mailIndex > index:
            if curr_message[mailIndex] == '>':
                return mailIndex + 1
            #else:
                #printError501()
        else:
            return -1
    #else:
        #printError501()
    return -1

def reversePath(index):
    global full_message
    pathIndex = path(index)
    if pathIndex > index:
        full_message += curr_message[index:pathIndex]
        full_message += '\n'
        return pathIndex
    else:
        return index

def forwardPath(index):
    global full_message, addresses
    pathIndex = path(index)
    if pathIndex > index:
        full_message += curr_message[index:pathIndex]
        full_message += '\n'
        addresses.append(curr_message[index+1:pathIndex-1])
        return pathIndex
    else:
        return index

def is2PartMessage(array1, array2):
    index = 0

    for character in array1:
        if curr_message[index] == character:
            index += 1

    if index == len(array1):
        if index >= len(curr_message):
            #printError501()
            return -2

        whitespaceIndex = whitespace(index)

        if whitespaceIndex > index:
            index = whitespaceIndex
        else:
            #printError501()
            return -2

        for character in array2:
            if curr_message[index] == character:
                index += 1

        if index - whitespaceIndex != len(array2):
            #printError500()
            return -1
    else:
        #printError500()
        return -1

    return index

def isData():
    data = ['D', 'A', 'T', 'A'];
    index = 0

    for character in data:
        if curr_message[index] == character:
            index += 1
        else:
            return False
    return True

def isMailFromCMD():
    global full_message
    index = is2PartMessage(['M','A','I','L'], ['F','R','O','M',':'])
    index503Rcpt = is2PartMessage(['R','C','P','T'], ['T','O',':'])
    index503Data = -1
    if isData():
        index503Data = 5

    if index503Rcpt >=  6 or index503Data == 5:
        return (False,503)

    if index < 9:
        return (False, 500)
    
    full_message = "FROM: "

    nullIndex = isNullspace(index)
    if nullIndex >= index:
        index = nullIndex
        reverseIndex = reversePath(index)
        if reverseIndex > index:
            index = reverseIndex
        else:
            return (False, 500)
    else:
        return (False, 501)

    nullIndex = isNullspace(index)
    if nullIndex >= index:
        index = nullIndex
    else:
        return (False,500)
    
    if isCRLF(index):
        return (True, 250)
    else:
        return (False, 501)

def isRcptToCMD():
    global full_message
    index = is2PartMessage(['R','C','P','T'], ['T','O',':'])
    index503Mail = is2PartMessage(['M','A','I','L'], ['F','R','O','M',':'])
    index503Data = -1
    if isData():
        index503Data = 5

    if index503Mail >= 9 or index503Data == 5:
        return (False, 503)

    if index < 7:
        return (False, 500)
    else:
        full_message += "TO: "

    nullIndex = isNullspace(index)
    if nullIndex >= index:
        index = nullIndex
    else:
        return (False, 500)

    forwardIndex = forwardPath(index)
    if forwardIndex > index:
        index = forwardIndex
    else:
        return (False, 501)
    
    if isCRLF(index):
        return (True, 250)
    else:
        return (False, 501)

def main():
    global curr_message, full_message, addresses
    state = "Mail" # Valid states are "Mail", "Rcpt/Data", "Message"
    for line in sys.stdin:
        curr_message = line
        errorCode = 0

        print(curr_message[:len(curr_message)-1])
        if state == "Mail":
            mailValue = isMailFromCMD()
            if mailValue[0]:
                state = "Rcpt/Data"
            errorCode = mailValue[1]
        elif state == "Rcpt/Data":
            rcptValue = isRcptToCMD()
            errorCode = rcptValue[1]
            if isData():
                if len(addresses) != 0:
                    state = "Message"
                    errorCode = 354
                else:
                    errorCode = 503
        elif state == "Message":
            if line == ".\n":
                state = "Mail"
                errorCode = 250
                for address in addresses:
                    messageToFile(address)
            else:
                full_message += line

        if errorCode == 500 and curr_message != "\n":
            printError500()
            state = "Mail"
        elif errorCode == 503:
            printError503()
            state = "Mail"
        elif errorCode == 501:
            printError501()
            state = "Mail"
        elif errorCode == 250:
            print250()
        elif errorCode == 354:
            print354()

main()
