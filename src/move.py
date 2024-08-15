
class Move:

    def __init__(self, inital, final, captured_piece=None):
        #intial and final are squares
        self.inital = inital
        self.final = final
        self.captured_piece = captured_piece

    def __str(self):
        s = ''
        s+= f'({self.inital.col}, {self.inital.row})'
        s += f' -> ({self.inital.col}, {self.final.row})'
        return s
    
    def __eq__(self,other):
        return self.inital == other.inital and self.final == other.final