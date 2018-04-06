class ElementSegment():
    '''
    Represents a element segment
    # TODO table
    '''

    def __init__(self,segment):
        self.index     = segment[0]   #table index
        self.offset    = segment[1:4] #i32 initializer expression
        self.numElems  = segment[4]   #number of elems
        #Place sequence of function indicies into a list
        self.elems     = [segment[i] for i in range(5, 5+self.numElems)]
    
    def size(self):
        '''
        Helper to determine size of an element segment
        '''
        return 5+self.numElems
        
class DataSegment():
    '''
    Represents a data segment
    '''
    def __init__(self,segment):
        self.index  = segment[0]   #table index
        self.offset = segment[1:4] #i32 initializer
        self.dataSize   = segment[4]   #size of data
        self.data   = [segment[i] for i in range (5, 5+self.dataSize)]
    def size(self):
        '''
        Helper to determine size of an data segment
        '''
        return 5+self.dataSize
