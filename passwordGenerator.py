from random import choice           #Importing the choice class from random module

lenOfPassword = 8       #setting the length of the password
validChars = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?'   #allowed chars
passwordList = []       #List to hold the output from choice() class

#function to generate the password with length, validChars, passwordList as arguments
def generatePassword(lenOfPassword, validChars, passwordList):
    try:
        for eachCharacter in range(lenOfPassword):      #iterating using the length of password
            passwordList.append(choice(validChars))     #appending the output of choice class to a list
        finalPassword = "".join(passwordList)           #creating the password string from list
        return finalPassword
    except Exception as e: 
        print("Issue generating the password : {}".format(e))
        return -1
    
def generatePasswordUsingListComprehension(lenOfPassword, validChars):
    try:
        finalPassword = "".join(choice(validChars) for eachCharacter in range(lenOfPassword))
        return finalPassword
    except Exception as e: 
        print("Issue generating the password : {}".format(e))
        return -1
    
if __name__=='__main__':
    generatePassword(lenOfPassword,validChars,passwordList)
    generatePasswordUsingListComprehension(lenOfPassword,validChars)
    

    



