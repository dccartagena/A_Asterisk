class nodo:
    def __init__(self, mapa):
        self.parent = None
        self.map = mapa
        self.child = []
        self.value = None
        self.pos = []
        self.prof = 0

    def changemap(self, pos):
        antpos = self.pos
        self.pos = pos
        self.map[self.pos[1], self.pos[2]] = 1
        self.map[antpos[1], antpos[2]] = 0

    def addchild(self, children):
        self.child.append(children)
        if self.child !=None:
            for node in self.child:
                node.parent = self
                node.prof = self.prof + 1

    def islisted(self, listarbol):
        check = False
        for i in listarbol:
            if self.map == i.map:
                check = True
        return check

