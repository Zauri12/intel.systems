import json

class Task:
    def __init__(self, title, description="", completed=False):
        self.title = title
        self.description = description
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["title"], data["description"], data["completed"])

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in data]
                print("Задачи успешно загружены.")
        except (FileNotFoundError, json.JSONDecodeError):
            print("Нет сохраненных задач или файл поврежден.")

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)
            print("Задачи успешно сохранены.")

    def display_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
        else:
            print("Список задач:")
            for index, task in enumerate(self.tasks, start=1):
                status = "✓" if task.completed else "✗"
                print(f"{index}. {task.title} [{status}] - {task.description}")

    def add_task(self, title, description=""):
        new_task = Task(title, description)
        self.tasks.append(new_task)
        print(f'Задача "{title}" добавлена.')

    def remove_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            removed_task = self.tasks.pop(task_index)
            print(f'Задача "{removed_task.title}" удалена.')
        else:
            print("Неверный индекс задачи.")

    def complete_task(self, task_index):
        if 0 <= task_index < len(self.tasks):
            self.tasks[task_index].completed = True
            print(f'Задача "{self.tasks[task_index].title}" выполнена.')
        else:
            print("Неверный индекс задачи.")

def main():
    task_manager = TaskManager()

    while True:
        print("\nВыберите действие:")
        print("1. Показать задачи")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("4. Завершить задачу")
        print("5. Сохранить задачи")
        print("0. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            task_manager.display_tasks()
        elif choice == "2":
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            task_manager.add_task(title, description)
        elif choice == "3":
            task_manager.display_tasks()
            task_index = int(input("Введите номер задачи для удаления: ")) - 1
            task_manager.remove_task(task_index)
        elif choice == "4":
            task_manager.display_tasks()
            task_index = int(input("Введите номер задачи для завершения: ")) - 1
            task_manager.complete_task(task_index)
        elif choice == "5":
            task_manager.save_tasks()
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()