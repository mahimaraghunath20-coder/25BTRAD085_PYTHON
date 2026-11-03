import csv

with open("payroll.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Employee Name", "Basic Salary", "Bonus", "Total Salary"])

    n = int(input("Enter number of employees: "))

    for i in range(n):
        name = input("Enter employee name: ")
        salary = float(input("Enter basic salary: "))
        bonus = float(input("Enter bonus: "))

        total = salary + bonus

        writer.writerow([name, salary, bonus, total])

print("\nPayroll details saved successfully!")

print("\n----- PAYROLL DETAILS -----")

with open("payroll.csv", "r") as file:
    reader = csv.reader(file)

    for row in reader:
        print(row)