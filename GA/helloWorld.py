import random
from math import pow

""" Code based on the post
https://burakkanber.com/blog/machine-learning-genetic-algorithms-part-1-javascript/
by Burak Kanber

"""

class Chromosome:
    def __init__(self, code=None):
        if (code):
            self.code = code
        else:
            self.code = ""
            
        self.cost = 9999

    def random(self, length):
        while(length):
            length -= 1
            self.code += chr(random.randrange(226))
            
    def calcCost(self, compareTo):
        total = 0
        for pos, i in enumerate(self.code):
            total += int(pow(ord(i) - ord(compareTo[pos]), 2))

        self.cost = total

    def mate(self, chrom):
        pivot = len(self.code)//2 - 1
        child1 = self.code[0:pivot] + chrom.code[pivot:]
        child2 = chrom.code[0:pivot] + self.code[pivot:]

        return Chromosome(child1), Chromosome(child2)

    def mutate(self, chance):
        if random.random() > chance:
            return None

        else:
            index = random.randrange(len(self.code))
            UporDown = 1
            if random.random() < chance:
                UporDown= -1
            newChar = chr(abs(ord(self.code[index]) + UporDown))
            newString = ""
            for pos, char in enumerate(self.code):
                if pos == index:
                    newString += newChar
                else:
                    newString += char

            self.code = newString

        return None

    def __str__(self):
        return self.code

    def __repr__(self):
        print(self.code)

class Population:
    
    def __init__(self, goal, size):
        self.members = []
        self.goal = goal
        self.generationNumber = 0
        while(size):
            size -= 1
            chrom = Chromosome()
            chrom.random(len(goal))
            self.members.append(chrom)

    def sort(self):
        self.members.sort(key=lambda x: x.cost)

    def generation(self):
        for member in self.members:
            member.calcCost(self.goal)

        self.sort()
        self.display()

        self.members.extend(self.members[0].mate(self.members[1]))

        for member in self.members:
            member.mutate(0.5)
            member.calcCost(self.goal)
            if member.code == self.goal:
                self.sort()
                self.display()
                return True

        self.generationNumber += 1
        return False

    def display(self):
        self.__repr__()
        
    def __repr__(self):
        for i in sorted(self.members, key=lambda x: x.cost, reverse=True):
            print(str(i), "(", i.cost, ") - ", self.generationNumber)


p = Population("Hello, world!", 50)

while(not p.generation()):
    pass
