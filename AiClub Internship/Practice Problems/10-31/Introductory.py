""" ----------------------  These are the introductory problem solutions --------------------------------"""

# Reverser
def reverser(x): # initialize function with parameter x - can be called whatever you want
    reversed = "" # initialize new reverse variable - we will be returning this
    for i in range(len(x) - 1, -1, -1): # The first parameter is the start, second is stop, third is step
        reversed += x[i] #Add character to reversed string
    reversed.swapcase() # This function changed all elements in string to opposite case
    return(reversed)



#Alphabet Soup
def alhpabetSoup(x):
    y = ""
    x = sorted(x.lower())# gives us a list of all characters in sorted order
    for i in range(len(x)):
        y += x[i] # Adds each character in list to new string

    return y

#Palindromes
def countPalindromes(start, stop):
    numPalindromes = 0
    
    if(start > stop or start < 0 or stop < 0):
        print("Parameter Error")
        return -1 # We don't want to raise an error with values

    #Start with Single Digits
    for i in range(start, stop + 1):
        palStr = str(i)
        revStr = palStr[::-1] # The [::-1] means we are reversing the order when slicing the string. This can also be used in the first problem.
        if (palStr == revStr):
            numPalindromes += 1
    return numPalindromes

#Test Cases
if __name__ == "__main__":
    print("\nReverser\n")
    print(reverser("Hello World"))
    print(reverser("ReVeRsE"))
    print(reverser("Radar"))

    # Alphabet Soup    
    print('\nAlphabet Soup\n')
    print(alhpabetSoup('hello'))
    print(alhpabetSoup('edabit'))
    print(alhpabetSoup('hacker'))
    print(alhpabetSoup('geek'))
    print(alhpabetSoup('javascript'))

    print("\nCount Palindromes\n")
    print(countPalindromes(1, 10))
    print(countPalindromes(555, 556))
    print(countPalindromes(878, 898))