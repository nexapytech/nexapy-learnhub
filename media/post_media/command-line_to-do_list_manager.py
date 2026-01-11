# todo.py
import json
import os

FILE = "tasks.json"

def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def show_tasks(tasks):
    if not tasks:
        print("✅ No tasks yet!")
    else:
        for i, task in enumerate(tasks, start=1):
            status = "✔️" if task["done"] else "❌"
            print(f"{i}. {status} {task['title']}")

def add_task(tasks, title):
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Added: {title}")

def complete_task(tasks, index):
    try:
        tasks[index]["done"] = True
        save_tasks(tasks)
        print(f"Completed: {tasks[index]['title']}")
    except IndexError:
        print("❗ Invalid task number")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- TO-DO LIST ---")
        show_tasks(tasks)
        print("\nOptions: [a]dd, [c]omplete, [q]uit")
        choice = input("Choose: ").strip().lower()

        if choice == "a":
            title = input("Task: ").strip()
            add_task(tasks, title)
        elif choice == "c":
            num = int(input("Task number: ")) - 1
            complete_task(tasks, num)
        elif choice == "q":
            break
        else:
            print("❗ Invalid choice")

if __name__ == "__main__":
    main()
