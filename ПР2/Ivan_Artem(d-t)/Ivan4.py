
tasks = []

try:
    with open("tasks.txt", "r+", encoding="utf-8") as f:
        tasks = []
        for i in f:
            _ = i.split(",  ")
            tasks.append({"desc": _[0], "done": _[1]})
except FileNotFoundError:
    with open("tasks.txt", "w", encoding="utf-8") as f:
        pass
    


# отображает все задачи в списке с их индексами
def display_tasks(task_list):
    return_string = ""
    for i in range(len(task_list)):
        return_string += "индекс: " + str(i) + ", задача: " + str(task_list[i].get("desc")) + ", статус выполнения: " + ("выполнено\n" if int(task_list[i].get("done")) == 1 else "не выполнено\n")
    return return_string

# добавляет новую задачу в список
def add_task(task_list, description):
    if ", " in description:
        print("описание задачи не может содержать разделители!") 
    elif len(description) != 0:
        task_list.append({"desc": str(description), "done": 0}) 
    else:
        print("описание задачи не должно быть пустым!")

    filing(task_list)

# отмечает задачу по индексу как выполненную
def mark_task_done(task_list, index):
    try:
        task_list[int(index)]["done"] = 1
        filing(task_list)
    except IndexError:
        print("такого индекса не существует! В данный момент индексы находятся в диапазоне от 0 до " + str(len(task_list)-1) + " включительно")
    except:
        print("неправильный формат ввода. Индекс должен быть целым неотрицательным числом")


# удаляет задачу по индексу
def delete_task(task_list, index):
    error_message = "неправильный формат ввода. Индекс должен быть целым неотрицательным числом"
    try:
        del task_list[int(index)]
        filing(task_list)
    except IndexError:
        print("такого индекса не существует! В данный момент индексы находятся в диапазоне от 0 до " + str(len(task_list)-1) + " включительно")
    except (TypeError, ValueError):
        print(error_message)
    

# возвращает общее количество задач
def get_task_count(task_list):
    return str(len(task_list))

# записывает данные в файл при выходе
def filing(task_list):
    try:
        with open("tasks.txt", "w", encoding="utf-8") as f:
            for task in task_list:
                line = f"{task['desc']},  {task['done']}\n"
                f.write(line)
    except Exception as e:
        print(f"произошла ошибка при сохранении файла: {e}")    

#меню
def main_menu(task_list):
    def safe_input(prompt):
        while True:
            try:
                return input(prompt).strip()
            except KeyboardInterrupt:
                return "7"
            except Exception as e:
                print(f"произошла непредвиденная ошибка при вводе: {e}")
    
    commands = {
        "1": lambda: print("\n" + display_tasks(task_list)),
        "2": lambda: add_task(task_list, safe_input("введите описание задачи: ")),
        "3": lambda: mark_task_done(task_list, safe_input("введите индекс задачи: ")),
        "4": lambda: delete_task(task_list, safe_input("введите индекс задачи: ")),
        "5": lambda: print("\n" + get_task_count(task_list)),
        "6": lambda: print(menu)
    }

    menu = """МЕНЕДЖЕР СПИСКА ЗАДАЧ

введите 1, если хотите: отобразить все задачи в списке,
введите 2, если хотите: добавить новую задачу в список,
введите 3, если хотите: отметить задачу по индексу как выполненную,
введите 4, если хотите: удалить задачу по индексу,
введите 5, если хотите: вернуть кол-во задач,
введите 6, если хотите: повторно отобразить меню,
введите 7, если хотите: выйти из менеджера"""
    
    print(menu)
    inp = ""
    while inp != "7":
        inp = safe_input("\nвведите номер необходимого действия: ") 

        if inp in commands:
            commands[inp]()
        elif inp == "7":
            filing(task_list)
            print("\nсписок задач сохранен в tasks.txt перед выходом")
            print("\nосуществлен выход из менеджера задач.")
        else:
            print("\nнеправильный формат ввода. Ознакомьтесь с инструкцией повторно:\n")
            print(menu)


if __name__ == "__main__":
    main_menu(tasks)
