attendance = {}

while True:
    print("\n----- ATTENDANCE TRACKER -----")
    print("1. Add Student")
    print("2. Update Attendance")
    print("3. Display Attendance")
    print("4. Calculate Attendance Percentage")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter student name: ")

        if name not in attendance:
            attendance[name] = []
            print("Student added successfully!")
        else:
            print("Student already exists!")

    elif choice == "2":
        name = input("Enter student name: ")

        if name in attendance:
            status = input("Enter attendance (P/A): ").upper()

            if status == "P" or status == "A":
                attendance[name].append(status)
                print("Attendance updated!")
            else:
                print("Enter P for Present or A for Absent.")
        else:
            print("Student not found!")

    elif choice == "3":
        print("\n----- ATTENDANCE DETAILS -----")

        for name, records in attendance.items():
            print(name, ":", records)

    elif choice == "4":
        name = input("Enter student name: ")

        if name in attendance:
            records = attendance[name]
            total = len(records)
            present = records.count("P")

            if total > 0:
                percentage = (present / total) * 100
                print("Attendance Percentage:", percentage, "%")
            else:
                print("No attendance records available.")
        else:
            print("Student not found!")

    elif choice == "5":
        print("Exiting Attendance Tracker.")
        break

    else:
        print("Invalid choice!")