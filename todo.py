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

def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"✅ Added: {title}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Use 'add' to create one.")
        return
    print("\n--- To-Do List ---")
    for i, t in enumerate(tasks, start=1):
        status = "✔" if t["done"] else "✗"
        print(f"{i}. [{status}] {t['title']}")

def mark_done(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        if tasks[index - 1]["done"]:
            print("Task already marked as done.")
        else:
            tasks[index - 1]["done"] = True
            save_tasks(tasks)
            print(f"🎯 Marked done: {tasks[index - 1]['title']}")
    else:
        print("Invalid task number!")

def main():
    print("Simple To-Do App")
    print("Commands: add <task>, list, done <number>, exit")

    while True:
        cmd = input("\n> ").strip().split(" ", 1)
        action = cmd[0].lower()

        if action == "add":
            if len(cmd) == 2 and cmd[1].strip():
                add_task(cmd[1].strip())
            else:
                print("Usage: add <task title>")
        elif action == "list":
            list_tasks()
        elif action == "done":
            if len(cmd) == 2 and cmd[1].isdigit():
                mark_done(int(cmd[1]))
            else:
                print("Usage: done <task number>")
        elif action == "exit":
            print("Goodbye!")
            break
        else:
            print("Unknown command! Try: add, list, done, exit")

if __name__ == "__main__":
    main()
