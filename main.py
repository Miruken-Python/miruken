# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from core import handles, handles2, handlers


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


class MyCallback:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"MyCallback({self.name})"


@handles
def handle(message: MyCallback):
    print(f'Hello from top level function, {message}')


class MyHandler:
    @handles
    def handle(self, message: MyCallback):
        print(f'Hello, {message}')


class MyHandler2:
    @handles2
    def handle(self, message: MyCallback):
        print(f'Hello @handles2, {message}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handlers.handle(MyCallback("Craig"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
