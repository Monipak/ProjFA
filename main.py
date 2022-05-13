from enum import auto
from venv import create
from Automaton import Automaton
from os.path import exists

from tools import *
global names

running = True
automatons = []
strings = []


def list_automatons(args):
    print(str(len(automatons))+" loaded automaton(s)")


def quit(args):
    global running
    running = False

def flush(args):
    global automatons
    automatons = []

def display(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            print("\nAutomaton n°",i)
            automatons[ind].display()
        else:
            print(
                "Index out of range, you can check the list of loaded automatons with the command list")
    elif args == "all":
        for i in range(len(automatons)):
            print("\nAutomaton n°",i)
            automatons[i].display()
    else:
        print("Invalid argument, disp takes an integer as argument")


def create_deter(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if is_deterministic(automatons[ind]):
                print("This automaton is already deterministic !")
                return #shhhhhhhh
            automatons.append(deter(automatons[ind]))
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, determine takes an integer as argument")

def create_minimal(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            automatons.append(deter(automatons[ind]))
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, determine takes an integer as argument")


def create_complete(args):
    if args.isdigit():
        ind = int(args)
        if ind < len(automatons):
            if is_complete(automatons[ind]):
                print("This automaton is already complete!")
                return 
            automatons.append(complete(automatons[ind]))
        else:
            print("Index out of range, you can check the list of loaded automatons with  the command list")
    else:
        print("Invalid argument, determine takes an integer as argument")


def load(args):
    if exists("txt/int4-1-"+args+".txt"):
        new = Automaton()
        new.load(args)
        automatons.append(new)
        print("int4-1-"+args+".txt loaded")
    else:
        print("Unable to load int4-1-"+args+".txt. Make sure it's in txt/ and try again")


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
        print(' '*8 + "name - loads the file 'txt/int4-1-name.txt into memory")

    elif args == "list":
        print("\nLIST")

    elif args == "quit":
        print("\nQUIT [-s]")
        print(' '*8 + "-s saves every automaton in memory")

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


commands = {"help": doc, "quit": quit, "load": load,"list": list_automatons,
        "disp": display, "determine": create_deter, "complete":create_complete,
        "flush":flush}


def parse(entree):
    global commands
    entree = entree.lower()
    entree = entree.split(' ') + ['']

    if entree[0] in commands:
        commands[entree[0]](entree[1])
    else:
        print("Invalid command, type help for a list of commands")


while running:
    parse(input())
    print()
