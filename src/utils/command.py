from types import LambdaType

command_list:dict[str, LambdaType] = {}

def command(command_name:str) :
    global command_list
    def wrapper(func):
        command_list[command_name] = func

    return wrapper

def call(command_name:str, *args):
    global command_list
    try:
        func = command_list[command_name]
        func(*args)
    except:
        raise Exception(f"There is no command {command_name} registered, Please check for any spelling mistakes or order of registeration")