import json
import os
import getpass

USERS_FILE = "users.json"

class TaskManager:
    def __init__(self):
        self.current_user = None
        self.tasks = []

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

    def register(self):
        users = self.load_users()
        username = input("Choose a username: ")
        if username in users:
            print("❌ Username already exists.\n")
            return
        password = getpass.getpass("Choose a password: ")
        users[username] = password
        self.save_users(users)
        print("✅ Registered successfully.\n")

    def login(self):
        users = self.load_users()
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        if users.get(username) == password:
            self.current_user = username
            self.load_tasks()
            print(f"✅ Welcome, {username}!\n")
            return True
        else:
            print("❌ Invalid username or password.\n")
            return False

    def get_task_file(self):
        return f"tasks_{self.current_user}.json"

    def load_tasks(self):
        try:
            with open(self.get_task_file(), "r") as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open(self.get_task_file(), "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self):
        title = input("Enter task title: ")
        self.tasks.append({"title": title, "completed": False})
        self.save_tasks()
        print("✅ Task added.\n")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks found.\n")
            return
        print("\n📋 Your Tasks:")
        for idx, task in enumerate(self.tasks, 1):
            status = "✅" if task["completed"] else "❌"
            print(f"{idx}. {task['title']} - {status}")
        print()

    def mark_task_completed(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to mark as completed: ")) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index]["completed"] = True
                self.save_tasks()
                print("✅ Task marked as completed.\n")
            else:
                print("❌ Invalid task number.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")

    def delete_task(self):
        self.view_tasks()
        try:
            index = int(input("Enter task number to delete: ")) - 1
            if 0 <= index < len(self.tasks):
                del self.tasks[index]
                self.save_tasks()
                print("🗑️ Task deleted.\n")
            else:
                print("❌ Invalid task number.\n")
        except ValueError:
            print("❌ Please enter a valid number.\n")

    def run(self):
        while True:
            print("====== Task Manager ======")
            print("1. Register")
            print("2. Login")
            print("0. Exit")
            choice = input("Choose an option: ")
            print()

            if choice == '1':
                self.register()
            elif choice == '2':
                if self.login():
                    self.task_menu()
            elif choice == '0':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice.\n")

    def task_menu(self):
        while True:
            print("------ Task Menu ------")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Delete Task")
            print("0. Logout")
            choice = input("Choose an option: ")
            print()

            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.mark_task_completed()
            elif choice == '4':
                self.delete_task()
            elif choice == '0':
                print(f"👋 Logged out from {self.current_user}\n")
                self.current_user = None
                self.tasks = []
                break
            else:
                print("❌ Invalid choice.\n")

# Run the app
if __name__ == "__main__":
    app = TaskManager()
    app.run()
