#Identity matrix
def identityMatrix(n):
    if n >= 0:
        iCounter = 0
    else:
        iCounter = abs(n) - 1
    idMatrix = []
    for i in range(abs(n)):
        idMatrix.append([])
        for j in range(abs(n)):
            if j == iCounter:
                idMatrix[i].append(1)
            else:
                idMatrix[i].append(0)
        if n >= 0:
            iCounter += 1
        else:
            iCounter -= 1                    
    return idMatrix

#Prime Factorization
def primeFactorization(n):
    primeList = []
    deadNum = False
    while not deadNum:
        for i in range(2, n + 1):
            if n % i == 0:
                primeList.append(i)
                n  = int(n / i)
            if n == 1:        
                deadNum = True

    return sorted(primeList)

#Word Overlapping
def wordOverlapping(a, b):
    c = a + b
    for i in range(len(a)):
        if a[i] == b[0]:
            d = i
            e = 0
            while a[d] == b[e]:
                d +=1
                e +=1
                if d == len(a) or e == len(b):
                    break
            print('pass')
            if d == len(a):
                #word connection found
                c = a + b[e:len(b)]
    return c

if __name__ == "__main__":
    print("\Identity Matrix\n")
    print(identityMatrix(2))
    print(identityMatrix(-2))
    print(identityMatrix(0))

    print("\Prime Factorization\n")
    print(primeFactorization(20))
    print(primeFactorization(100))
    print(primeFactorization(8912234))

    print("\nWord Overlapping\n")
    print(wordOverlapping("honey", "milk"))
    

