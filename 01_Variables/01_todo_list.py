import os

TODO_FILE = "files/todo.txt"


def load_todos():
    if not os.path.isfile(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return [line.strip('\n') for line in f.readlines()]
    except OSError as e:
        print(f"--error reading file: {e}--")
        return []


def save_todos(todos):
    try:
        with open(TODO_FILE, "w") as f:
            for item in todos:
                f.write(item + "\n")
    except OSError as e:
        print(f"--error saving file: {e}--")


def add_todo(todos):
    while True:
        todo = input("enter a todo (or 'exit' to stop adding): ")
        if todo == "exit":
            break
        if not todo.strip():
            print("--todo cannot be empty--")
            continue
        todos.append(todo)
    save_todos(todos)


def get_valid_number(todos):
    """Запрашивает номер и проверяет, что это корректное число и индекс существует."""
    raw = input("enter a number: ")
    try:
        number = int(raw) - 1
    except ValueError:
        print("--please enter a valid number--")
        return None

    if 0 <= number < len(todos):
        return number
    else:
        print("--invalid number--")
        return None


def edit_todo(todos):
    number = get_valid_number(todos)
    if number is None:
        return
    new_todo = input("Enter a new todo: ")
    if not new_todo.strip():
        print("--todo cannot be empty--")
        return
    todos[number] = new_todo
    save_todos(todos)


def complete_todo(todos):
    number = get_valid_number(todos)
    if number is None:
        return
    todos.pop(number)
    save_todos(todos)


def show_todos(todos):
    if not todos:
        print("--list is empty--")
        return
    print("--list--")
    for index, item in enumerate(todos):
        print(index + 1, '-', item)


def main():
    os.makedirs("files", exist_ok=True)
    todos = load_todos()
    user_prompt = "type add, edit, complete or show:"

    while True:
        try:
            user_action = input(user_prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n--exiting--")
            break

        match user_action:
            case "add":
                add_todo(todos)
            case "edit":
                edit_todo(todos)
            case "complete":
                complete_todo(todos)
            case "show":
                show_todos(todos)
            case "exit":
                break
            case _:
                print("--unknown command--")


if __name__ == "__main__":
    main()