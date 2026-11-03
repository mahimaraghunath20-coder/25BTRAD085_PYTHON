print("----- BILL GENERATOR -----")

name = input("Enter customer name: ")
item = input("Enter item name: ")
price = float(input("Enter item price: "))
quantity = int(input("Enter quantity: "))

total = price * quantity

print("\n----- CUSTOMER BILL -----")
print("Customer Name:", name)
print("Item:", item)
print("Price:", price)
print("Quantity:", quantity)
print("Total Amount:", total)

print("Thank you for shopping!")