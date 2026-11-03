filename = input("Enter log file name: ")

try:
    with open("25BTRAD085_Lab Exercises/" + filename, "r") as file:
        content = file.readlines()

    error = 0
    warning = 0
    info = 0

    for line in content:
        if "ERROR" in line:
            error += 1
        elif "WARNING" in line:
            warning += 1
        elif "INFO" in line:
            info += 1

    print("\n----- LOG SUMMARY -----")
    print("ERROR:", error)
    print("WARNING:", warning)
    print("INFO:", info)

    if len(content) == 0:
        print("Log file is empty.")

except FileNotFoundError:
    print("File not found!")