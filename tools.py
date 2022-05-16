from tkinter import N
from Automaton import Automaton
# deepcopy copie tout ce qui est dynamique dans un objet (leeeeeeeeeent)
from copy import deepcopy as copy

#------------------USEFUL FUNCTIONS-------------------------------
def union(l1 : list, l2 : list) -> list:
    n = l1.copy()
    for i in l2:
        if i not in n:
            n.append(i)
    n.sort()
    return n

def divide_part(automaton: Automaton, partition : list, group : list) -> list:
    """Divides a partition, based wether each element is in or out of 'group' """
    patterns = {} #stores the whole table as patterns, uses a dictionary to refer ourselves to 'automaton' 's states
    for state in partition:
        trans = automaton.table[state]
        pattern = {}
        for char in trans: #We are confident doing this as the DFA is complete
            pattern[char] = trans[char][0] in group # True/False patterns
        patterns[state] = pattern
    
    seen_patterns = [] 
    new_partitions = [] #Both are stored in the same order, length is at most 2^alphabet_length

    for state in partition:
        if patterns[state] not in seen_patterns:
            seen_patterns.append(patterns[state])
            new_partitions.append([state])
        else:
            new_partitions[seen_patterns.index(patterns[state])].append(state) #adds a state at the index with a matching pattern

    return new_partitions

def from_parts(base: Automaton, partitions : list) -> Automaton:
    """Constructs an automaton from a partition and a base automaton
    not necessary but improves readability
    """
    new = Automaton()
    new.univ = base.univ.copy()

    new_states = {} #map: member of each subgroup (original states) -> new_state

    for new_state, pseudo in enumerate(partitions): 
        new.alias[new_state] = str(pseudo)[1:-1].replace(' ','') #enables to see original states in the display
        for state in pseudo:
            new_states[state] = [new_state]
            if state in base.end:
                new.end.append(new_state)
            if state in base.ini:
                new.ini.append(new_state)


    for i in range(len(partitions)): #constructs the new table
        trans = {}
        for char in new.univ:
            jmp = base.table[partitions[i][0]][char][0] #takes the first transition of the first element 
            #Takes the first transition in the pseudo-state i, and stores in jmp its destination through 'char'
            trans[char] = new_states[jmp]
        new.table.append(trans)

    return new

            



#---------------------OPERATIONS-----------------------------

def minimise(base: Automaton) -> Automaton:
    """Transforms a CDFA to a MCDFA"""
    partitions = [list(range(len(base.table)))] # = [ [0,1,...,n] ], logically the first partition is the whole automaton.
    done = False
    while not done:
        new_parts = partitions.copy()

        if len(partitions) == 1: #This only happens at the first iteration
            new_parts.remove(partitions[0]) #we remove the partition, as it will be replaced by the spanned sub-groups
            for part in divide_part(base, partitions[0], base.end): #As this is the first iteration, the checked group is the outputs
                new_parts.append(part)
        else:
            for part in partitions:
                new_parts.remove(part)
                for part in divide_part(base, part, part): #At any other iteration, we only check if its in or out
                    new_parts.append(part)

        new_parts.sort(key= lambda l: l[0]) #we need to sort to enable list comparisons
        if new_parts == partitions:
            done = True
            if len(partitions) == 1:
                print("This automaton is already minimal !")
        else:
            print("NEW PARTS",new_parts)
        partitions = new_parts

    return from_parts(base, partitions) #now that we have our transitions, we can build a new automaton with them.

def check(automaton: Automaton, string: str) -> bool:  # wont work with an asynchronous automaton (epsilon loops are hard to detect and curb, we need to do the e-closure fist)
    """Checks wether a string is validated by an automaton"""
    cursors = automaton.ini.copy() #places cursors at the initial states
    table = automaton.table

    for char in string:
        n_cursors = cursors.copy()
        for cur in cursors:
            n_cursors.remove(cur) #we remove the old cursors


        for cur in cursors:
            if table[cur].get(char):
                for path in table[cur].get(char): #if the char does not exist, it wont iterates as get will return None
                    if path not in n_cursors:
                        n_cursors.append(path) #and we place them along

        cursors = n_cursors

    for cur in cursors:
        if cur in automaton.end: #at the end, if we have cursors in the final states, the word passes the check
            return True
    return False

def standard(automaton: Automaton) -> Automaton:
    """Standardises a FA"""
    new = copy(automaton)
    trans = {}
    for state in new.ini: #iterates through every initial states
        for char in new.table[state]: #retrieves their transitions
            if char not in trans:
                trans[char] = new.table[state][char].copy()
            else:
                trans[char] = union(new.table[state][char].copy(),
                                    trans[char])

    #appends it to the end
    new.table.append(trans)
    new.ini = [len(new.table)-1]

    return new

def e_connected(automaton : Automaton, state : int) -> list:
    pseudo_state =[state]
    if automaton.table[state].get('*'):
        for e_jump in automaton.table[state]['*']:
            if e_jump not in pseudo_state:
                for st in e_connected(automaton, e_jump): #Recursivity is the best way to scan a graph when memory is not an issue
                    pseudo_state.append(st)
    pseudo_state.sort()
    return pseudo_state

def synchronise(base: Automaton) -> Automaton:
    new = Automaton()
    new.univ = base.univ.copy()
    new.univ.remove('*') #We do not want to iterate on the * char
    
    new.ini = [0]

    e_groups = []
    for i in range(len(base.table)): #We determine every possible e_closure from each state
        e_groups.append(e_connected(base, i))

    pending = [[]]
    for initial in base.ini:
        pending[0] = union(pending[0],e_groups[initial])

    pseudo_states = [pending[0]]
    state = 0
    while pending:
        trans = {}
        pseudo_trans = {}
        pseudo_state = pending.pop(0)

        for i in pseudo_state: #Here we merge the transitions of the pseudostates into one transition
            if i in base.end and state not in new.end: #if any of the member state is in the finals, the pseudo-state gets in the finals
                new.end.append(state)
            for char in new.univ:
                if base.table[i].get(char):
                    for tran in base.table[i][char]:
                        if not trans.get(char):
                            trans[char] = e_groups[tran] #Particularity : we link transitions to the whole e_connected group
                        else:
                            trans[char] = union(trans[char], e_groups[tran])

        for char in trans:
            if trans[char] not in pseudo_states:
                pseudo_states.append(trans[char])

            index = pseudo_states.index(trans[char])
            if trans[char] not in pending and index > state:
                pending.append(trans[char])
            pseudo_trans[char] = [index]
        
        new.table.append(pseudo_trans)
        state += 1
    
    for i in range(len(pseudo_states)):
        new.alias[i] = str(pseudo_states[i])[1:-1].replace(' ','')

    return new
#--------------------e_closure will be develloped for the presentation !!! ---------------------------


def deter(base: Automaton) -> Automaton:
    """Determines an automaton"""
    new = Automaton()
    pseudo_states = [base.ini.copy()] #the first pseudo_state, which is the initial states
    new.ini = [0]

    pending = [base.ini.copy()]  # untreated states, used like a queue

    state = 0
    while pending:
        trans = {}
        pseudo_trans = {}
        pseudo_state = pending.pop(0)

        for i in pseudo_state: #Here we merge the transitions of the pseudostates into one transition
            if i in base.end and state not in new.end: #if any of the member state is in the finals, the pseudo-state gets in the finals
                new.end.append(state)
            
            for char in base.table[i]: 
                if char not in new.univ:
                    new.univ.append(char)

                if not trans.get(char):
                    trans[char] = base.table[i][char].copy()
                else:
                    trans[char] = union(base.table[i][char], trans[char])

        for char in trans: #We then translate to the new actual states
            if trans[char] not in pseudo_states:
                pseudo_states.append(trans[char])

            index = pseudo_states.index(trans[char])
            if trans[char] not in pending and index > state:
                pending.append(trans[char]) #the new index is stored in a list of size 1, like every transition state
            pseudo_trans[char] = [index]

        new.table.append(pseudo_trans.copy())


        state += 1
    for i in range(len(pseudo_states)):
        new.alias[i] = str(pseudo_states[i])[1:-1].replace(' ','') #This enables us to display with the old states
    return new

def complete(base: Automaton) -> Automaton:
    """Appends a bin to an automaton to make it complete"""
    new = copy(base)
    index = len(base.table)
    bin_trans = {} #transition of the bin
    for char in base.univ:
        bin_trans[char] = [index]
        for i in range(len(new.table)): #for each state, if there is no transition for 'char', we make it point tower the end (the bin)
            if not new.table[i].get(char): 
                new.table[i][char] = [index]
    new.table.append(bin_trans)
    return new

def complement(automaton: Automaton) -> Automaton:
    """Reverses every output of an automaton"""
    new = copy(automaton)
    for i in range(len(automaton.table)):
        if i in automaton.end:
            new.end.remove(i)
        else:
            new.end.append(i)

    return new

#-----------------------------CHECKS-------------------------------------------------
def is_standard(base: Automaton) -> bool:
    if len(base.ini) != 1: #Only one input
        return False
    else:
        for trans in base.table: 
            for char in trans:
                if base.ini[0] in trans[char]: #and no transition going to the input
                    return False
    return True

def is_complete(base: Automaton) -> bool:
    
    for trans in base.table:
        if len(trans) != len(base.univ): #Each transition row should is defined for every character
            return False
    return True

def is_deterministic(base: Automaton) -> bool:
    if len(base.ini) != 1: #One entry
        return False

    for trans in base.table:
        for action in trans:
            if len(trans[action]) > 1: #No ambiguous transition
                return False
    return True

def is_synchronous(base: Automaton) -> bool:
    return '*' not in base.univ

if __name__ == "__main__":
    a = Automaton()
    a.load('31')
    a.display()
    a = synchronise(a)
    a.display()
    a.display_alias()
    print(a.ini,a.end)