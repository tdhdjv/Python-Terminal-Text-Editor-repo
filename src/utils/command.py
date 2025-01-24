from types import LambdaType

command_list:dict[str, LambdaType] = {}

def command(*command_names:str) -> None:
    global command_list
    def wrapper(func):
        for command_name in command_names:
            command_list[command_name] = func

    return wrapper

def call(command_name:str, *args) -> None:
    global command_list
    
    try:
        func = command_list[command_name]
        func(*args)
    except (TypeError, KeyError) as e:
        if isinstance(e, KeyError):
            raise KeyError(f"There is no function called '{command_name}' registered! Check for spelling mistakes \n Commands List: {command_list}")
        elif isinstance(e, TypeError):
            raise e
