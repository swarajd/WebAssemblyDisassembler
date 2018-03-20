class Section:
    def populate(self, inputBytes):
        self.sectionCode = int.from_bytes(inputBytes[0:1],byteorder='little', signed=False)
        self.sectionSize = int.from_bytes(inputBytes[1:2],byteorder='little', signed=False)
        self.numTypes    = int.from_bytes(inputBytes[2:3],byteorder='little', signed=False)
        self.data        = inputBytes[3:self.sectionSize+2]
        print(vars(self))
        return inputBytes[self.sectionSize+2:] #return remaining bytes

def makeSectionList(inputBytes):
    sectionList = [None]*11
    for i in range (0, len(sectionList)):
        if (inputBytes != None):
            section    = Section()
            inputBytes = section.populate(inputBytes)
            sectionList[section.sectionCode] = section
    return sectionList
