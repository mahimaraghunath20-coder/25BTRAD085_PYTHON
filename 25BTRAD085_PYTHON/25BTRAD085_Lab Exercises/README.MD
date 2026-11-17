# Smart Campus: Digital Attendance System
# Non-Preemptive Priority Scheduling

# Process details:
# [Process ID, Task Name, Arrival Time, Burst Time, Priority]

processes = [
    ["P1", "Attendance Report", 0, 10, 3],
    ["P2", "QR Check-in", 0, 2, 1],
    ["P3", "QR Check-in", 0, 3, 1],
    ["P4", "Save Attendance", 0, 4, 2]
]


def priority_scheduling(processes):

    n = len(processes)
    completed = []
    current_time = 0

    total_waiting_time = 0
    total_turnaround_time = 0

    print("\nNON-PREEMPTIVE PRIORITY SCHEDULING")
    print("-" * 65)

    print(f"{'Process':<10}{'Task':<22}{'Waiting Time':<16}{'Turnaround Time'}")
    print("-" * 65)

    while len(completed) < n:

        available = []

        # Find processes that have arrived and are not completed
        for process in processes:
            if process not in completed and process[2] <= current_time:
                available.append(process)

        # Select the process with the highest priority
        # Smaller priority number means higher priority
        selected = min(
            available,
            key=lambda x: (x[4], x[2])
        )

        process_id = selected[0]
        task_name = selected[1]
        arrival_time = selected[2]
        burst_time = selected[3]

        # Calculate waiting time
        waiting_time = current_time - arrival_time

        # Execute the process completely
        current_time += burst_time

        # Calculate turnaround time
        turnaround_time = current_time - arrival_time

        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time

        completed.append(selected)

        print(
            f"{process_id:<10}{task_name:<22}"
            f"{waiting_time:<16}{turnaround_time}"
        )

    # Calculate averages
    average_waiting_time = total_waiting_time / n
    average_turnaround_time = total_turnaround_time / n

    print("-" * 65)
    print("Average Waiting Time:", average_waiting_time)
    print("Average Turnaround Time:", average_turnaround_time)

    print("\nExecution Order:")
    for process in completed:
        print(process[0], end=" -> ")

    print("END")


# Display process details
print("SMART CAMPUS ATTENDANCE SYSTEM")
print("\nProcess Details:")
print("Priority 1 = Highest Priority")
print("Priority 3 = Lowest Priority")

# Run Priority Scheduling
priority_scheduling(processes)Python Lab Exercises
