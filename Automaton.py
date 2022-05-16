class Automaton():
    def __init__(self):
        self.univ = [] #Alphabet
        self.table = [] #list of dictionaries, 1 per state (char -> [state(s)])
        
        self.ini = [] 
        self.end = []

        self.alias = {} #used only for display (state->string)
        

    def load(self, file_name):
        with open("txt/int4-1-"+file_name+".txt",'r') as fstream:
            i = 0
            for line in fstream:
                transitions = {}
                line = line.replace('\n','')

                if line:
                    for split in line.split(' '):
                        #checks for final / initial flags
                        if split[0] == 'I':
                            self.ini.append(i)
                        elif split[0] == 'F':
                            self.end.append(i)
                        elif split[0] == 'B':
                            self.ini.append(i)
                            self.end.append(i)

                        else:
                            if split[0] not in self.univ: #adds unknown characters
                                self.univ.append(split[0])
                            
                            transition = []
                            for j in range(1, len(split)): #skips the first character, which is the transition's character
                                transition.append(int(split[j]))
                            
                            transitions[split[0]] = transition #map it to the said character
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

    def display_alias(self): #only works with DFAs
        to_disp =' '*15
        tran = ''
        for char in self.univ:
            to_disp += char + ' '*12


        for i in range(len(self.table)):

            if i in self.ini and i in self.end:
                to_disp += "\n<> "+ self.alias[i]
            elif i in self.ini:
                to_disp += "\n-> "+ self.alias[i]
            elif i in self.end:
                to_disp += "\n<- "+ self.alias[i]
            else:
                to_disp += "\n   "+ self.alias[i]
            to_disp += ' '*(11-len(self.alias[i])) + "║ "
            for char in self.univ:
                if self.table[i].get(char):
                    tran = str(self.alias[self.table[i][char][0]])
                    tran += (11-len(tran))*' '
                else:
                    tran = ' '*11 
                to_disp+= tran+"║ "
        
        print(to_disp)


    def raw_disp(self): #used for debugging purposes
        for i in self.table:
            print(i)