#Square Patch

def squarePatch(n):
    nList = []
    for i in range(n):
        nList.append([])
        for j in range(n):
            nList[i].append(n)
    return nList


def squaresAndCubes(x, y):
    a = x ** (1./2)
    b = y ** (1./3)
    if a == b:
        return True
    return False

def mysteryFunc(num):
    product = 1
    numStr = str(num)
    for i in numStr:
        product *= int(i)
    return product

if __name__ == "__main__":
    print("\nSquare Patch\n")
    print(squarePatch(3))
    print(squarePatch(5))
    print(squarePatch(1))
    print(squarePatch(0))
    print('\nSquares and Cubes\n')
    print(squaresAndCubes(4, 8))
    print(squaresAndCubes(16, 48))
    print(squaresAndCubes(9, 27))
    print('\nMystery Func\n')
    print(mysteryFunc(152))
    print(mysteryFunc(832))
    print(mysteryFunc(19))
    print(mysteryFunc(133))



