from enum import auto
from xmlrpc.client import Boolean
from Automaton import Automaton
from copy import deepcopy as copy #deepcopy copie tout ce qui est dynamique dedans

def union(l1,l2):
    res = l1.copy()
    for i in l2:
        if i not in res:
            res.append(i)
    res.sort()
    return res

def check(automaton : Automaton, string : str) -> bool: #ne marche pas avec le char vide !!
    cursors = automaton.ini.copy()
    table = automaton.table

    for char in string:
        n_cursors = cursors.copy()
        for cur in cursors:
            n_cursors.remove(cur)
        for cur in cursors:
            if table[cur].get(char):
                for path in table[cur].get(char):
                    if path not in n_cursors:
                        n_cursors.append(path)
        
        cursors = n_cursors

    for cur in cursors:
        if cur in automaton.end:
            return True
    
    return False

def standard(automaton : Automaton) -> Automaton:
    new = copy(automaton)
    trans = {}
    for state in new.ini:
        for char in new.table[state]:
            if char not in trans:
                trans[char] = new.table[state][char].copy()
            else:
                for jump in new.table[state][char]:
                    if jump not in trans[char]:
                        trans[char].append(jump)
    
    new.table.append(trans)
    new.ini = [len(new.table)-1]

    return new

def deter(base : Automaton) -> Automaton:
    new = Automaton()
    pseudo_states = [base.ini.copy()]
    new.ini = [0]

    stake = [base.ini.copy()] #états non traités, utilisé comme une pile

    state = 0
    while stake:
        trans = {}
        alias_trans = {}
        pseudo_state = stake.pop()
        #fusion des transitions des pseudo états
        for i in pseudo_state:
            if i in base.end and state not in new.end:
                new.end.append(state)
            for char in base.table[i]:
                if char not in new.univ:
                    new.univ.append(char)

                if not trans.get(char):
                    trans[char] = base.table[i][char].copy()
                else:
                    trans[char] = union(base.table[i][char], trans[char])

        
        for char in trans:
            if trans[char] not in pseudo_states:
                    pseudo_states.append(trans[char])

            index = pseudo_states.index(trans[char])
            if trans[char] not in stake and index > state:
                stake.append(trans[char])
            alias_trans[char] = [index] # dans la nouvelle transition, on mets l'index qui correspond au pseudo état, on as une liste de taille 1

        new.table.append(alias_trans.copy())

        
        state += 1

    return new



def complete(base: Automaton) -> Automaton:
    new = copy(base)
    index = len(base.table)
    bin_trans = {}
    for char in base.univ:
        bin_trans[char] = [index]
        for i in range(len(new.table)):
            if not new.table[i].get(char):
                new.table[i][char] = [index]
    new.table.append(bin_trans)
    return new

    

def complement(automaton : Automaton) -> Automaton: #ne passer qu'un déter !!!
    new = copy(automaton)
    for i in range(len(automaton.table)):
        if i in automaton.end:
            new.end.remove(i)
        else:
            new.end.append(i)

    return new 


def is_standard(base: Automaton) -> bool:
    if len(base.ini) != 1:
        return False
    else:
        for trans in base.table:
            for char in trans:
                if base.ini[0] in trans[char]:
                    return False
    return True

def is_complete(base: Automaton) -> bool:
    for trans in base.table:
        for char in base.univ:
            if not trans.get(char):
                return False
    return True

if __name__ == "__main__":
    a = Automaton()
    a.load("test")
    a.display()

    a = standard(a)
    a = complete(a)
    a.display()

    a = deter(a)
    a.display()


    #pass