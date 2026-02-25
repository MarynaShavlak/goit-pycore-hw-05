from typing import Tuple, List, Dict


def input_error(func):
    """
    Decorator for handling user input errors.

    Catches:
    - ValueError
    - KeyError
    - IndexError

    Returns appropriate user-friendly messages
    without stopping program execution.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter the required arguments for this command."
        except ValueError as e:
            return str(e) if str(e) else "Invalid input."
    return inner

def parse_input(user_input: str) -> Tuple[str, ...]:
    """
    Parses raw user input into a command and its arguments.

    The input string is split by whitespace.
    The first word is treated as the command (converted to lowercase),
    and the remaining words are returned as unpacked arguments.

    Args:
        user_input (str): The raw input string entered by the user.

    Returns:
        Tuple[str, ...]:
            A tuple where:
            - the first element is the command (str),
            - the remaining elements are arguments (str).

    Example:
        Input:  "add John 1234567890"
        Output: ("add", "John", "1234567890")
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def validate_phone(phone: str) -> None:
    """
    Raises ValueError if phone is invalid.
    """
    if not phone.isdigit():
        raise ValueError("Wrong phone format. It must contain only digits.")

    if len(phone) != 10:
        raise ValueError("Wrong phone format. It must contain 10 digits.")

@input_error
def add_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Adds a new contact to the contacts dictionary.

    Args:
        args (List[str]): A list containing [name, phone].
        contacts (Dict[str, str]): Dictionary storing contacts
                                   in the format {name: phone}.

    Returns:
        str:
            - Success confirmation message.
            - Error message if arguments are invalid or phone is incorrect.
    """
    if len(args) != 2:
        raise ValueError("Give me name and phone please.")

    name, phone = args  #  IndexError
    validate_phone(phone) #  ValueError
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Updates the phone number of an existing contact.

    Args:
        args (List[str]): A list containing [name, new_phone].
        contacts (Dict[str, str]): Dictionary storing contacts.

    Returns:
        str:
            - Success confirmation message if updated.
            - Error message if contact does not exist or input is invalid.
    """
    if len(args) != 2:
        raise ValueError("Give me name and new phone please.")

    name, phone = args #  IndexError

    if name not in contacts:
        raise KeyError #  KeyError

    validate_phone(phone) #  ValueError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args: List[str], contacts: Dict[str, str]) -> str:
    """
    Retrieves the phone number for a specific contact.

    Args:
        args (List[str]): A list containing [name].
        contacts (Dict[str, str]): Dictionary storing contacts.

    Returns:
        str:
            - The formatted contact string "name: phone".
            - Error message if contact does not exist or arguments are invalid.
    """
    if len(args) != 1:
        raise ValueError("Enter user name.")  # ValueError

    name = args[0] # IndexError
    return f"{name}: {contacts[name]}" # KeyError

@input_error
def show_all(contacts: Dict[str, str]) -> str:
    """
    Returns a formatted string containing all saved contacts.

    Contacts are sorted alphabetically by name.

    Args:
        contacts (Dict[str, str]): Dictionary storing contacts.

    Returns:
        str:
            - A formatted multi-line string of contacts.
            - A message if no contacts are stored.
    """
    if not contacts:
        return "No contacts found."

    return "\n".join(
        f"{name}: {phone}"
        for name, phone in sorted(contacts.items())
    )


def show_help() -> str:
    """
    Returns a formatted string listing all available commands.

    Returns:
        str: Help message with command descriptions.
    """
    return """
Available commands:
- hello: Greet the bot
- add [name] [phone]: Add a new contact
- change [name] [new_phone]: Change an existing contact's phone number
- phone [name]: Show the phone number of a contact
- all: Show all contacts
- help: Show this help message
- close, exit: Exit the bot
"""


def main():
    """
    Entry point of the assistant bot.

    Initializes the contacts dictionary and starts
    an interactive command loop until the user exits.
    """
    contacts: Dict[str, str] = {}

    commands = {
        "hello": lambda args: "How can I help you?",
        "add": lambda args: add_contact(args, contacts),
        "change": lambda args: change_contact(args, contacts),
        "phone": lambda args: show_phone(args, contacts),
        "all": lambda args: show_all(contacts),
        "help": lambda args: show_help(),
    }

    print("Welcome to the assistant bot!")
    print(show_help())

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        if command in commands:
            print(commands[command](args))
        else:
            print("Invalid command. Please use one of the following commands:")
            print(show_help())

if __name__ == "__main__":
    main()
