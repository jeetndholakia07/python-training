def calculate_bill(*prices,**tax):
    totalAmount, taxAmount, finalAmount = 0,0,0
    for price in prices:
        totalAmount+=price

    taxAmount = (totalAmount * tax.get("tax"))/100
    finalAmount = totalAmount + taxAmount

    return {
        "Total Amount":totalAmount,
        "Tax Amount":taxAmount,
        "Payable Amount":finalAmount
    }

userInput = input("Enter arguments space separated (e.g. 100 200 300 tax=18):").split(" ")
amounts = []
tax = {}
try:
    for item in userInput:
        if("=" in item):
            key,val = item.split("=")
            tax[key] = int(val)
        else:
            amounts.append(int(item))
    result = calculate_bill(*amounts, **tax)
    for key,val in result.items():
        print(f"{key} : {val}")
except (ValueError,TypeError):
        print("Invalid format. Please provide integer value.")