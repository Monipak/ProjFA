
from Automaton import Automaton
from os.path import exists


from tools import *
global names

running = True
automatons = []
strings = []


def list_automatons(args):
    print(str(len(automatons))+" loaded automaton(s)")

def add(args):
    global strings
    inp = input("Enter strings to test for the automatons : ")
    while inp != "done":
        if '*' in inp:
            print("Invalid string, cannot contain '*'")
        else:
            strings.append(inp)
            inp = input(
                "Enter a string to test for the automaton, or 'done' to stop : ")

def checks(args):
    global strings
    global automatons
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if not is_synchronous(automatons[ind]):
                new = synchronise(automatons[ind])
            else:
                new = automatons[ind]
            for strn in strings:
                print(strn,check(new,strn))
        else:
            print(
                "Index out of range, you can check the list of loaded automatons with the command list")
    else:
        print("Invalid argument, disp takes an integer as argument")


def quit(args):
    global running
    running = False


def flush(args):
    if not args:
        automatons = []
        print("Flushed the automatons !")
    elif args == "strings":
        strings = []
        print("Flushed the testing batch !")
    else:
        print("Invalid argument, flush takes 'strings'/nothing as argument")

def display(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            print("\nAutomaton n°",ind)
            automatons[ind].display()
        else:
            print(
                "Index out of range, you can check the list of loaded automatons with the command list")
    elif args == "all":
        for i in range(len(automatons)):
            print("\nAutomaton n°", i)
            automatons[i].display()
    else:
        print("Invalid argument, disp takes an integer/'all' as argument")


def create_deter(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if is_deterministic(automatons[ind]):
                print("This automaton is already deterministic !")
            elif not is_synchronous(automatons[ind]):
                print("This automaton is not synchronous, please synchronise it using sync.")
            else:
                print("Added the determinised automaton at index "+ str(len(automatons)) +'!')
                automatons.append(deter(automatons[ind]))
                print("\nIn terms of old states :")
                automatons[-1].display_alias()
        else:
            print(
                "Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, determine takes an integer as argument")




def create_complete(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if is_complete(automatons[ind]):
                print("This automaton is already complete!")
            elif not is_synchronous(automatons[ind]):
                print("This automaton is not synchronous, please synchronise it using sync.")
            else:
                print("Added the completed automaton at index "+ str(len(automatons)) +'!')
                automatons.append(complete(automatons[ind]))
        else:
            print(
                "Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, complete takes an integer as argument")

def create_minimal(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if not is_deterministic(automatons[ind]) or not is_complete(automatons[ind]):
                print("This automaton is not deterministic and/or complete !")
            elif not is_synchronous(automatons[ind]):
                print("This automaton is not synchronous, please synchronise it using sync.")
            else:
                print("Added the minimised automaton at index "+ str(len(automatons)) +'!')
                automatons.append(minimise(automatons[ind]))
                print("\nIn terms of old states :")
                automatons[-1].display_alias()
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, minimise takes an integer as argument")

def create_synchronised(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if  is_synchronous(automatons[ind]):
                print("This automaton already synchronous !")
            else:
                print("Added the synchronised automaton at index "+ str(len(automatons)) +'!')
                automatons.append(synchronise(automatons[ind]))
                print("\nIn terms of old states :")
                automatons[-1].display_alias()
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, synchronise takes an integer as argument")

def create_complement(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if not is_deterministic(automatons[ind]) or not is_complete(automatons[ind]):
                print("This automaton is not deterministic and/or complete !")
            else:
                print("Added the complementarised automaton at index "+ str(len(automatons)) +'!')
                automatons.append(synchronise(automatons[ind]))
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, synchronise takes an integer as argument")

def load(args):
    if exists("txt/int4-1-"+args+".txt"):
        new = Automaton()
        new.load(args)
        automatons.append(new)
        print("int4-1-"+args+".txt loaded")
    else:
        print("Unable to load int4-1-"+args +
              ".txt. Make sure it's in txt/ and try again")


def add(args):
    global strings
    inp = input("Enter a string to test for the automaton : ")
    while inp != "done":
        strings.append(inp)
        inp = input(
            "Enter a string to test for the automaton, or 'done' to stop : ")

def batch(args):
    print(strings)

def doc(args):
    global commands

    if args == '':
        print("\nAvailable commands :")
        for cmd in commands:
            print(cmd)
    elif "-all" in args:
        for cmd in commands:
            doc(cmd)
    elif args not in commands:
        print("Cannot find help for '", args,
              "', type 'help' for a list of commands", sep='')
    elif args == "help":
        print("\nHELP [command] [-all]")
        print(' '*8 + "command - displays the usage of command")
        print(' '*8 + "-all - displays the usage of every command")

    elif args == "load":
        print("\nLOAD name")
        print(' '*8 + "name - loads the file 'txt/name.txt into memory")

    elif args == "add":
        print("\nADD")
        print("Allows to add strings to the testing batch")

    elif args == "list":
        print("\nLIST")

    elif args == "quit":
        print("\nQUIT")
        print(' '*8 + "Quits the program")

    elif args == "disp":
        print("\nDISP index")
        print(' '*8 + "index - displays the automaton at the given index")

    elif args == "determine":
        print("\nDETERMINE index")
        print(
            ' '*8 + "index - saves a determinized copy of the automaton at the given index")
    elif args == "complete":
        print("\nCOMPLETE index")
        print(
            ' '*8 + "index - saves a complete copy of the automaton at the given index")
    elif args == "minimise":
        print("\nMINIMISE index")
        print(
            ' '*8 + "index - saves a minimised copy of the automaton at the given index")
    elif args == "sync":
        print("\nSYNC index")
        print(
            ' '*8 + "index - saves a synchronised copy of the automaton at the given index")
    elif args == "flush":
        print("\nFLUSH")
        print(
            ' '*8 + "flushes the list of automatons from memory")
    elif args == "batch":
        print("\nBATCH")
        print(
            ' '*8 + "shows the batch of strings to test")
    elif args == "complement":
        print("\nCOMPLEMENT index")
        print(
            ' '*8 + "index - saves a complementarised copy of the automaton at the given index")


commands = {"help": doc, "quit": quit, "load": load,"list": list_automatons,
        "disp": display, "determine": create_deter, "complete":create_complete,
        "flush":flush,"add_strings":add,"check":checks,"minimise":create_minimal,"sync":create_synchronised,
        "batch":batch,"complement":create_complement}


def parse(entree):
    global commands
    entree = entree.lower()
    entree = entree.split(' ') + ['']

    if entree[0] in commands:
        commands[entree[0]](entree[1])
    else:
        print("Invalid command, type help for a list of commands")

print("Enter a command, or help for a list of command (help command gives documentaiton about a command)")
while running:
    parse(input())
    print()
