import sys

STATE0=0;SYMBOL0=1;STATE1=3;SYMBOL1=4;MOVE=5

def gen_key(state, symbol):
    return "%s:%s" % (state, symbol)

HEAD="H";TAIL="T";NODE="N"
BLANK="_"

class Tape:
    def __init__(self):
        self.head = TapeNode(ntype=HEAD)
        self.tail = TapeNode(ntype=TAIL)

        self.head.next = self.tail
        self.tail.prev = self.head
        
        self.curr = None
        
    def append_node(self, node):
        prev = self.tail.prev

        prev.next = node
        node.prev = prev

        node.next = self.tail
        self.tail.prev = node

        if not self.curr:
            self.curr = self.head.next


    def insert_before_node(self, node, refnode):
        """
        Insert a node before the reference node.
        """
        prev = refnode.prev

        prev.next = node
        node.prev = prev

        node.next = refnode
        refnode.prev = node

    def move_left(self):
        self.curr = self.curr.prev

    def move_right(self):
        self.curr = self.curr.next

    def move(self, direction):
        if direction == ">":
            self.move_right()
        if direction == "<":
            self.move_left()

    def replace_curr_symbol(self, symbol):
        node = self.curr

        if symbol == node.char:
            return
        
        if symbol == BLANK:
            # delete node
            prev = node.prev
            next = node.next

            prev.next = next
            next.prev = prev
        else:
            if node.is_head():
                newnode = TapeNode(symbol)
                self.insert_before_node(newnode, node.next)
                self.curr = newnode
            elif node.is_tail():
                newnode = TapeNode(symbol)
                self.insert_before_node(newnode, self.tail)
                self.curr = newnode
            else:
                node.char = symbol
            
            
    def get_curr_symbol(self):
        if self.curr.is_head() or self.curr.is_tail():
            return BLANK
        
        return self.curr.char

    def dump(self):
        chars = []
        pos = self.head.next
        while not pos.is_tail():
            chars.append(pos.char)
            pos = pos.next

        print(chars)

    def dump_tape_status(self):
        chars = []
        pos = self.head.next
        while not pos.is_tail():
            if pos == self.curr:
                chars.append("(%s)" % pos.char)
            else:
                chars.append(pos.char)
            pos = pos.next

        s = ''.join(chars)
        print(s)


class TapeNode:
    def __init__(self, char=BLANK, ntype=NODE):
        self.nodetype = ntype
        self.char = char
        self.prev = None
        self.next = None

    def is_head(self):
        return self.nodetype == HEAD

    def is_tail(self):
        return self.nodetype == TAIL
        

class Tmachine:
    def __init__(self):
        self.tape = None
        self.state_diagram = {}
        self.num_of_states = 0

        self.cursor = 0
        self.state = 0

    def initialize(self, s):
        self.tape = Tape()
        
        for i in range(0, len(s)):
            char = s[i]
            
            node = TapeNode(char=char)
            self.tape.append_node(node)
            
    def simulate(self):
        while True:
            state0 = self.state
            symbol0 = self.tape.get_curr_symbol()
            
            self.tape.dump_tape_status()
            
            if int(state0) == self.num_of_states:
                print("accept")
                return

            key = gen_key(state0, symbol0)
        
            if not key in self.state_diagram:
                print("reject")
                return
        
            state1, symbol1, direction = self.state_diagram[key]
            #print(state0, symbol0, "->", state1, symbol1, direction)

            self.tape.replace_curr_symbol(symbol1)
            
            self.state = state1

            self.tape.move(direction)
            
            
    def dump(self):
        print("tape:")
        self.tape.dump_tape_status()
        
        print("states:", self.num_of_states)
        #for key in self.state_diagram:
        #    print(key, self.state_diagram[key])
    
    def read_tm_file(self, filename):
        with open(filename, 'r') as f:
            line = f.readline() # 1st line: # of states
            line = line.strip()
            tokens = line.split(':')
            
            self.num_of_states = int(tokens[1])
            
            line = f.readline() # 2nd line: alphabets
            line = f.readline()
            while line:
                tokens = line.split()

                state0  = tokens[STATE0]
                symbol0 = tokens[SYMBOL0]
                state1  = tokens[STATE1]
                symbol1 = tokens[SYMBOL1]
                move =  tokens[MOVE]

                key = gen_key(state0, symbol0)
                self.state_diagram[key] = [state1, symbol1, move]
            
                line = f.readline()



if __name__=='__main__':
    if len(sys.argv) < 2:
        print("usage: ", sys.argv[0], "<TM_file>")
        sys.exit(1)


    
    tmfile = sys.argv[1]

    tape = ""
    try:
        tape = input()
    except:
        pass
    
    tm = Tmachine()
    tm.initialize(tape)
    tm.read_tm_file(tmfile)
    #tm.dump()
    
    tm.simulate()
