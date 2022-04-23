class Automaton():
    def __init__(self):
        self.univ = []
        self.table = [] #array de dicos, 1 dico par état

        self.ini = []
        self.end = []

        self.alias = {}
        

    def load(self, file_name):
        with open("txt/int4-1-"+file_name+".txt",'r') as fstream:
            i = 0
            for line in fstream:
                transitions = {}
                for split in line.split(' '):
                    split = split.replace('\n', '')

                    if split[0].isupper(): #ajoute aux entrées/sorties si il y a un flag en majuscule
                        if split[0] == 'I':
                            self.ini.append(i)
                        elif split[0] == 'F':
                            self.end.append(i)
                        elif split[0] == 'B':
                            self.ini.append(i)
                            self.end.append(i)

                    else:
                        if split[0] not in self.univ: #ajoute un éventuel caractère inconnu
                            self.univ.append(split[0])
                        
                        transition = [] #liste des transitions avec ce caractère
                        for j in range(1, len(split)):
                            transition.append(int(split[j])) #en entiers
                        
                        transitions[split[0]] = transition #mis dans le dico
                i+=1

                self.table.append(transitions)

    def display(self):
        to_disp =' '*8
        tran = ''
        for char in self.univ:
            to_disp += char + ' '*10


        for i in range(len(self.table)):

            if i in self.ini and i in self.end:
                to_disp += "\n<> "+str(i)+" ║ "
            elif i in self.ini:
                to_disp += "\n-> "+str(i)+" ║ "
            elif i in self.end:
                to_disp += "\n<- "+str(i)+" ║ "
            else:
                to_disp += "\n   "+str(i)+" ║ "
            for char in self.univ:
                if self.table[i].get(char):
                    tran = str(self.table[i][char])[1:-1].replace(' ','')
                    tran += (9-len(tran))*' '
                else:
                    tran = ' '*9 
                to_disp+= tran+"║ "
        
        print(to_disp)

    def display_alias(self):
        to_disp =' '*8
        tran = ''
        for char in self.univ:
            to_disp += char + ' '*10


        for i in range(len(self.table)):

            if i in self.ini and i in self.end:
                to_disp += "\n<> "+ self.alias[i] +" ║ "
            elif i in self.ini:
                to_disp += "\n-> "+ self.alias[i] +" ║ "
            elif i in self.end:
                to_disp += "\n<- "+ self.alias[i] +" ║ "
            else:
                to_disp += "\n   "+ self.alias[i] +" ║ "
            for char in self.univ:
                if self.table[i].get(char):
                    for state in self.table[i][char]:
                        tran += self.alias[i] +','
                    tran += (9-len(tran))*' '
                else:
                    tran = ' '*9 
                to_disp+= tran+"║ "
        
        print(to_disp)


    def raw_disp(self):
        for i in self.table:
            print(i)


