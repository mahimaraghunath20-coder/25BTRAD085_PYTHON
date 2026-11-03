print("----- STUDENT GRADING SYSTEM -----")

name = input("Enter student name: ")

m1 = int(input("Enter marks in Subject 1: "))
m2 = int(input("Enter marks in Subject 2: "))
m3 = int(input("Enter marks in Subject 3: "))
m4 = int(input("Enter marks in Subject 4: "))
m5 = int(input("Enter marks in Subject 5: "))

total = m1 + m2 + m3 + m4 + m5
average = total / 5

print("\n----- STUDENT RESULT -----")
print("Student Name:", name)
print("Total Marks:", total)
print("Average:", average)

if average >= 90:
    print("Grade: A")
elif average >= 75:
    print("Grade: B")
elif average >= 60:
    print("Grade: C")
elif average >= 40:
    print("Grade: D")
else:
    print("Grade: Fail")