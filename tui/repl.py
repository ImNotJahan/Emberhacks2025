from latex_extension.data import MeasuredData
from llm_interface.request_manager import RequestsManager
from llm_to_server_glue            import parse_json
from server_to_latex_glue          import env
from os                            import path

manager = RequestsManager()

parsed_data    = dict()
evaluated_data = dict()

prompt_parsed    = lambda: print("Enter the name of a saved parsed equation")
prompt_evaluated = lambda: print("Enter the name of a saved evaluated equation")
eq_not_found     = lambda: print("Equation not found")
cmd_input        = lambda: input("# ")

def print_help(args: list[str]) -> None:
    print(
"""help\t See this dialog
parse\t Parse a human-readable equation
eval\t Evaluate a library-ready equation
steps\t View the steps of an evaluated equation
result\t View the result of an evaluated equation
exit\t Close this program
clear\t Clear the terminal
list\t List out any saved data
expr\t Run a python expression using an evaluated equation
save\t Save a parsed equation to disk
load\t Load a parsed equation from disk""")


def print_intro() -> None:
    print()
    print("Welcome to certainPY!")
    print()
    print_help([])
    print()
    print("To see this dialog again, just type \"help\"")


def unknown_command(args: list[str]) -> None:
    print("Unknown command")


def clear_terminal(args: list[str]) -> None:
    print("\033[H\033[2J", end="") # ANSI ESC code for clearing terminal & moving cursor to correct pos


def parse(args: list[str]) -> None:
    print("Enter an equation and any needed variables to evaluate it:")
    # have the AI parse it
    response = manager.get_response(cmd_input())

    # check if an error occurred
    if response[:5] == "[ERR]":
        print("An error occurred while parsing:", response[5:])
    else:
        print("Enter a name for this equation:")
        parsed_data[name := cmd_input()] = response
        print("Saved parsed equation as", name)


def evaluate(args: list[str]) -> None:
    if len(args) == 0:
        prompt_parsed()
        name = cmd_input()
    else:
        name = args[0]

    if name not in parsed_data:
        eq_not_found()
    else:
        variables, equation = parse_json(parsed_data[name])
        variables.update(env) # add trig functions

        evaluated_data[name] = eval(equation, variables)
        print("Saved evaluated equation as", name)


def run_expression(args: list[str]) -> None:
    if len(args) == 0:
        prompt_evaluated()
        name = cmd_input()
    else:
        name = args[0]

    if name not in evaluated_data:
        eq_not_found()
    else:
        if len(args) < 2:
            print("Enter your expression, using x as the name of the equation:")
            expression = cmd_input()
        else:
            expression = args[1]

        exec(expression, {"x": evaluated_data[name]})


def list_data(args: list[str]) -> None:
    print("Parsed data:", list(parsed_data.keys()))
    print("Evaluated data:", list(evaluated_data.keys()))


def save_parsing(args: list[str]) -> None:
    if len(args) == 0:
        prompt_parsed()
        name = cmd_input()
    else:
        name = args[0]

    if name not in parsed_data:
        eq_not_found()
    else:
        if len(args) < 2:
            print("Enter the filepath to save it to:")
            filepath = cmd_input()
        else:
            filepath = args[1]

        with open(filepath, "w") as f:
            f.write(parsed_data[name])

        print("Saved to", filepath)


def load_parsing(args: list[str]) -> None:
    if len(args) == 0:
        print("Enter a filepath to a saved parsing")
        filepath = cmd_input()
    else:
        filepath = args[0]

    if not path.exists(filepath):
        print("No such file exists:", filepath)
    else:
        if len(args) < 2:
            print("Enter a name for this equation:")
            name = cmd_input()
        else:
            name = args[1]

        with open(filepath, "r") as f:
            parsed_data[name] = f.read()
        print("Loaded as", name)


def view_result(args: list[str]) -> None:
    if len(args) == 0:
        prompt_evaluated()
        name = cmd_input()
    else:
        name = args[0]

    if name not in evaluated_data:
        eq_not_found()
    else:
        print(evaluated_data[name])


def view_steps(args: list[str]) -> None:
    if len(args) == 0:
        prompt_evaluated()
        name = cmd_input()
    else:
        name = args[0]

    if name not in evaluated_data:
        eq_not_found()
    else:
        dp = evaluated_data[name]

        if len(args) < 2:
            print("How would you like to view the steps? (Enter #)")
            print("0. Sequentially, rounded numbers & values inserted")
            print("1. Composed, rounded numbers & values inserted")
            print("2. Sequentially, unrounded & values inserted")
            print("3. Sequentially, rounded & values uninserted")
            print("4. Sequentially, unrounded & values uninserted")
            print("5. Composed, unrounded numbers & values inserted")
            print("6. Composed, rounded numbers & values uninserted")
            print("7. Composed, unrounded numbers & values uninserted")
            option = cmd_input()
        else:
            option = args[1]

        result = None

        match option:
            case "0":
                result = dp.all_steps_sequential(True, True)
            case "1":
                result = dp.all_steps_composite(True, True)
            case "2":
                result = dp.all_steps_sequential(True, False)
            case "3":
                result = dp.all_steps_sequential(False, True)
            case "4":
                result = dp.all_steps_sequential(False, False)
            case "5":
                result = dp.all_steps_composite(True, False)
            case "6":
                result = dp.all_steps_composite(False, True)
            case "7":
                result = dp.all_steps_composite(False, False)
            case _:
                print("Invalid option:", option)

        if result:
            if len(result) == 2:
                print("Value calculation:")
                print(result[0])
                print()
                print("Uncertainty calculation:")
                print(result[1])
            else:
                print("Value calculation\tUncertainty calculation\tData point")

                for step in zip(*result):
                    print("{}\t{}\t{}".format(*step))


def start_repl() -> None:
    commands = {
        "help": print_help, "exit": exit, "clear": clear_terminal, "list": list_data,
        "parse": parse, "eval": evaluate, "expr": run_expression,
        "save": save_parsing, "load": load_parsing,
        "result": view_result, "steps": view_steps
    }

    print_intro()

    while True:
        statements = input("$ ").split(";")

        for statement in statements:
            command = statement.split()

            if command:
                commands.get(command[0], unknown_command)(command[1:])