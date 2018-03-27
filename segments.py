class ElementSegment():
    '''
    Represents a element segment
    # TODO table
    '''

    def __init__(self,segment):
        #TODO make sure the bytes indexed are correct once example of elements is found  
        self.index     = segment[0]; #table index
        self.offset    = segment[1]; #i32 initilizer expression
        self.numElems  = segment[2]; #number of elems
        #Place sequence of function indicies into a list
        self.elems     = [segment[i] for i in range(3, 3+self.numElems)]
    
    def size(self):
        '''
        Helper to determine size of an element section
        '''
        # TODO idx probably wrong
        return 3+self.numElems
        
class DataSegment():
    # TODO
    pass
