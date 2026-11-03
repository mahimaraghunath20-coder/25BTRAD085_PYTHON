# Writing student details into a file

with open("students.txt", "w") as file:
    n = int(input("Enter number of students: "))

    for i in range(n):
        name = input("Enter student name: ")
        roll = input("Enter roll number: ")
        marks = input("Enter marks: ")

        file.write(name + "," + roll + "," + marks + "\n")

print("\nStudent details saved successfully!")

# Reading student details from the file

print("\n----- STUDENT DETAILS -----")

with open("students.txt", "r") as file:
    for line in file:
        print(line.strip())