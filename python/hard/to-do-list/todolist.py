from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from datetime import timedelta
from enum import Enum

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

    def __get_date(self):
        return self.deadline.strftime("%b %d")


class MenuChoice(Enum):
    TODAY = 1
    WEEK = 2
    ALL = 3
    MISSED = 4
    ADD = 5
    DELETE = 6
    EXIT = 0


class ToDoList:
    def __init__(self):
        self.__menu_choice = None
        self.__engine = create_engine("sqlite:///todo.db?check_same_thread=False")
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()
        self.__date_format = "%d %b"
        self.__weekdays = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

    def __menu(self):
        print("1) Today's tasks")
        print("2) Week's tasks")
        print("3) All tasks")
        print("4) Missed tasks")
        print("5) Add task")
        print("6) Delete task")
        print("0) Exit")
        self.__menu_choice = MenuChoice(int(input()))

    def __get_date_format(self, date):
        return date.strftime(self.__date_format).lstrip("0")

    def __get_week_day(self, date):
        return self.__weekdays[date.weekday()]

    def __get_day(self, is_today=False, day=datetime.today()):
        weekday = self.__get_week_day(day)
        if is_today:
            weekday = "Today"
        tasks = self.__session.query(Task).filter(Task.deadline == day.date()).all()
        today = f"\n{weekday}: {day.strftime(self.__date_format)}\n"
        result = ""
        for i, task in enumerate(tasks):
            result += f"{i + 1}. {task}\n"
        return today + ("Nothing to do!\n" if result == "" else result)

    def __add_new_task(self):
        print("Enter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        new_row = Task(task=task, deadline=datetime.strptime(deadline, "%Y-%m-%d"))
        self.__session.add(new_row)
        self.__session.commit()
        print("The task has been added!\n")

    def __get_week(self):
        today = datetime.today()
        result = ""
        for i in range(7):
            day = today + timedelta(days=i)
            result += self.__get_day(day=day)
        return result

    def __get_all_tasks(self, func_filter=True):
        tasks = self.__session.query(Task).order_by(Task.deadline).filter(func_filter).all()
        result = ""
        for i, task in enumerate(tasks):
            result += f"{i + 1}. {task}. {self.__get_date_format(task.deadline)}\n"
        return result

    def __get_missed_tasks(self):
        result = ""
        result += self.__get_all_tasks(func_filter=Task.deadline < datetime.today().date())
        return "Missed tasks:\n" + ("Nothing is missed!\n" if result == "" else result)

    def __delete_task(self):
        tasks = self.__get_all_tasks()
        if not tasks:
            print("Nothing to delete")
            return
        print("Choose the number of the task you want to delete:")
        print(tasks)
        choice = int(input())
        if self.__delete_task_by_timeline(choice):
            print("The task has been deleted!")
        else:
            print("Something goes wrong.")

    def __delete_task_by_timeline(self, number):
        try:
            tasks = self.__session.query(Task).order_by(Task.deadline).all()
            delete_row = tasks[number - 1]
            self.__session.delete(delete_row)
            self.__session.commit()
            return True
        except:
            return False

    def menu(self):
        while True:
            self.__menu()
            if self.__menu_choice == MenuChoice.TODAY:
                print(self.__get_day(is_today=True))
            if self.__menu_choice == MenuChoice.ADD:
                self.__add_new_task()
            if self.__menu_choice == MenuChoice.WEEK:
                print(self.__get_week())
            if self.__menu_choice == MenuChoice.ALL:
                print(self.__get_all_tasks())
            if self.__menu_choice == MenuChoice.MISSED:
                print(self.__get_missed_tasks())
            if self.__menu_choice == MenuChoice.DELETE:
                self.__delete_task()
            if self.__menu_choice == MenuChoice.EXIT:
                print("Bye!")
                break


if __name__ == '__main__':
    todo = ToDoList()
    todo.menu()
