numbers = input("Enter comma separated numbers:").split(",")
numList = []
sum = 0

try:
    for i in range(len(numbers)):
        numList.append(int(numbers[i]))
        sum+=int(numbers[i])
        
    print("List: ", numList)
    my_tuple = tuple(numList)
    print("Tuple: ", my_tuple)
    my_set = set(numList)
    print("Set: ", my_set)
    print("Sum: ", sum)

    print("Unique numbers:",end=" ")
    for i in my_set:
        print(i,end=" ")
    print()

    myList = numList.copy()
    myList.sort(reverse=True)
    print("Sorted List: ", myList)
except ValueError as e:
        print("Please enter comma separated integer values only.")