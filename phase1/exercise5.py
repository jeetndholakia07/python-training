def execution_logger(func):
    def inner(n):
        print("Starting function",n)
        print("Ending function",n)
        return func(n)
    return inner

@execution_logger
def factorial(n):
    if(n==1):
        return 1
    else:
        return n * factorial(n-1)
    
try:
    num = int(input("Enter n :"))
    fact = factorial(num)
    print(f"Factorial of {num} is {fact}")
except ValueError:
    print("Please enter integer values only")