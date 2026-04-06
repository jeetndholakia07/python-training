import sys

def calculate_bill(*prices, **tax):
    totalAmount, taxAmount, finalAmount = 0, 0, 0
    for price in prices:
        totalAmount += price

    taxAmount = (totalAmount * tax.get("tax")) / 100
    finalAmount = totalAmount + taxAmount

    return {
        "Total Amount": totalAmount,
        "Tax Amount": taxAmount,
        "Payable Amount": finalAmount,
    }

# Get command line arguments
args = sys.argv[1:]
amounts = []
tax = {}
try:
    for item in args:
        if "=" in item:
            key, val = item.split("=")
            tax[key] = int(val)
        else:
            amounts.append(int(item))
    if len(amounts) == 0 or not tax.get("tax"):
        raise ValueError("Invalid format. Please provide amounts.")
    result = calculate_bill(*amounts, **tax)
    for key, val in result.items():
        print(f"{key} : {val}")
except (ValueError, TypeError):
    print("Invalid format. Please provide integer value.")