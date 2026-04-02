checkDivisible = lambda num,div : num % div == 0

def generatorFunction(n):
    for i in range(1,n):
        yield i

try:
    n = int(input("Enter number:"))
    for i in generatorFunction(n):
        if(checkDivisible(i,3) and checkDivisible(i,5)):
            print("FizzBuzz")
        elif(checkDivisible(i,3)):
            print("Fizz")
        elif(checkDivisible(i,5)):
            print("Buzz")
        else:
            print(i)
except ValueError:
    print("Please enter integer values only.")