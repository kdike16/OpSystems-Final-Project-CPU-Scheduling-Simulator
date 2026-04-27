from scheduler import Scheduler
from process import Process

def main():

    while True:
        print("\nSelect Scheduling Algorithm:")
        print("F  - FCFS")
        print("S  - SJF")
        print("T  - SRTF")
        print("P  - Priority (Non-Preemptive)")
        print("PP - Priority (Preemptive)")
        print("R  - Round Robin")
        print("Q  - Quit")

        choice = input("Enter choice: ").strip().upper()

        if choice == 'Q':
            print("Exiting...")
            break

        # Create fresh scheduler each run
        scheduler = Scheduler()

        # Re-add processes each time
        scheduler.addProcess(Process(1, 0, 8, 3))
        scheduler.addProcess(Process(2, 1, 4, 1))
        scheduler.addProcess(Process(3, 2, 2, 2))

        algorithm_map = {
            'F': scheduler.schedule_Next,
            'S': scheduler.schedule_Shortest_Job,
            'T': scheduler.schedule_Shortest_Remaining_Time,
            'P': scheduler.schedule_Priority_NonPreemptive,
            'PP': scheduler.schedule_Priority_Preemptive,
            'R': scheduler.schedule_Round_Robin
        }

        selected = algorithm_map.get(choice)

        if selected is None:
            print("Invalid choice. Try again.")
            continue

        if selected == scheduler.schedule_Round_Robin:
            quantum = int(input("Enter time quantum: "))
            scheduler.run(selected, quantum=quantum)
        else:
            scheduler.run(selected)


if __name__ == "__main__":
    main()