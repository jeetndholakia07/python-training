def even_numbers(n):
    for i in range(0,n+1):
        if(i%2==0):
            yield i

numbers = []
check = lambda num, x : num > x

try:
    n = int(input("Enter n :"))
    for i in even_numbers(n):
        if(check(i,10)):
            numbers.append(i)
    print(f"Final List: ",numbers)
except ValueError:
    print("Please enter integer values only")