import sys

from general import General
from random import randint
from general_state import GeneralState

GENERALS = list()


def arg_parser(args: list[str]) -> int:
    if len(args) != 2:
        print(f"Usage: {args[0]} number_of_processes.\nExample: $ {args[0]} 2.", file=sys.stderr)
        exit(1)
    try:
        num_of_processes = int(args[1])
        if num_of_processes < 1:
            print(f"Number of processes should be >= 1. Got: {num_of_processes}", file=sys.stderr)
            exit(1)
        return num_of_processes
    except:
        print(f"Number of processes should be positive integer. Got: {args[1]}", file=sys.stderr)
        exit(1)


def cli_handler(command: str):
    command = command.strip().split()
    if not command:
        return
    if command[0] == "actual-order":
        if len(command) != 2 or (command[1] != "attack" and command[1] != "retreat"):
            print("Usage: actual-order [order] where order is attack/retreat", file=sys.stderr)
        else:
            if command[1] == "attack":
                pass
            elif command[1] == "retreat":
                pass
            k = len(list(filter(lambda g: g.state == GeneralState.FAULTY, GENERALS)))
            if len(GENERALS) < 3 * k + 1:
                print(
                    "Execute order: cannot be determined – not enough generals in the system! "
                    f"{k} faulty node(s) in the system - {len(GENERALS) - k} out of {len(GENERALS)} quorum "
                    "not consistent")
    elif command[0] == "g-state":
        if len(command) == 1:
            for general in GENERALS:
                print(f"G{general.id}, {general.role()}, state={general.state}")
        elif len(command) == 3:
            command[2] = command[2].lower()
            if command[2] != "faulty" and command[2] != "non-faulty":
                print("Usage: g-state [general_id] [faulty/non-faulty]", file=sys.stderr)
            else:
                for general in GENERALS:
                    if general.id == int(command[1]):
                        if command[2] == "faulty":
                            general.state = GeneralState.FAULTY
                        else:
                            general.state = GeneralState.NON_FAULTY
                    print(f"G{general.id}, state={general.state}")
        else:
            print("Usage: g-state [id] [state]\n or: g-state", file=sys.stderr)
    elif command[0] == "g-kill":
        if len(command) == 2:
            for i, general in enumerate(GENERALS):
                if general.id == int(command[1]):
                    GENERALS.pop(i)
                    # TODO: In case primary is deleted, new primary selected automatically
            for general in GENERALS:
                print(f"G{general.id}, state={general.state}")
        else:
            print("Usage: g-kill [id]", file=sys.stderr)
    elif command[0] == "g-add":
        if len(command) == 2:
            if int(command[1]) > 0:
                highest_id = GENERALS[-1].id
                for i in range(1, int(command[1]) + 1):
                    GENERALS.append(General(highest_id + i, False))
            else:
                print("Number of generals to add should be a positive integer", file=sys.stderr)
        else:
            print("Usage: g-add [num_of_generals]", file=sys.stderr)
    else:
        print(f"Unknown command: {command[0]}", file=sys.stderr)


def main(argv):
    num_processes = arg_parser(argv)

    for i in range(1, num_processes + 1):
        GENERALS.append(General(i, False))
    primary = randint(0, num_processes - 1)
    GENERALS[primary].primary = True
    for general in GENERALS:
        general.start()

    while True:  # TODO: condition to stop/stop only on keyboard interrupt?
        command = input("$ ")
        try:
            cli_handler(command)
        except Exception as _:
            print("Error while handling command!", file=sys.stderr)
        except KeyboardInterrupt:
            exit(0)


if __name__ == "__main__":
    main(sys.argv)
