from constants import *
from type import *

class ImportEntry:
    def __init__(self, inputBytes):
        """
        field       type            description
        ---------------------------------------------------------
        moduleLen   varuint32       length of moduleStr in bytes
        moduleStr   bytes           module name: valid UTF-8 byte sequence
        fieldLen    varuint32       length of fieldStr in bytes
        fieldStr    bytes           field name: valid UTF-8 byte sequence
        kind        external_kind   the kind of definition being imported

        Followed by, if the kind is Function:
        kindType        varuint32       type index of the function signature

        or, if the kind is Table:
        kindType        table_type      type of the imported table

        or, if the kind is Memory:
        kindType        memory_type     type of the imported memory

        or, if the kind is Global:
        kindType        global_type     type of the imported global
        """
        self.moduleLen = inputBytes[0]
        self.moduleStr = inputBytes[1:1 + self.moduleLen].decode('utf-8')

        self.fieldLen = inputBytes[1 + self.moduleLen]
        fieldStrIndex = 2 + self.moduleLen
        self.fieldStr = inputBytes[fieldStrIndex:fieldStrIndex + self.fieldLen].decode('utf-8')

        # kind is one of the values found in EXTERNAL_KIND_TABLE.
        # Depending on the value of kind, the kindType maybe an integer(function kind) or an array.
        # Therefore, the length (kindLen) is dependent on the kind as well.
        # For function, because it is an integer, it will be a length of 1.
        # For the remaining kind types, the length is equal to the length of the array.
        self.kind = EXTERNAL_KIND_TABLE[inputBytes[fieldStrIndex + self.fieldLen]]
    
        if self.kind is 'function':
            self.kindType = inputBytes[fieldStrIndex + self.fieldLen + 1]
            self.kindLen = 1

        elif self.kind is 'table':
            self.kindType = TableType(inputBytes[fieldStrIndex + self.fieldLen + 1])
            self.kindLen = kindType.size()

        elif self.kind is 'memory':
            self.kindType = MemoryType(inputBytes[fieldStrIndex + self.fieldLen + 1])
            self.kindLen = kindType.size()

        elif self.kind is 'global':
            self.kindType = GlobalType(inputBytes[fieldStrIndex + self.fieldLen + 1])
            self.kindLen = kindType.size()

        else:
            raise ValueError('Invalid kind type')

    def size(self):
        return 3 + self.moduleLen + self.fieldLen + self.kindLen

    def to_str(self):
        return 'ImportEntry: (module: {}, field: {}, kind_value: {})'.format(self.moduleStr, self.fieldStr, self.kindType)

class ExportEntry:
    """
    field          type            description
    ---------------------------------------------------------
    exportNameLen  varuint32       length of moduleStr in bytes
    exportNameStr  bytes           export name: valid UTF-8 byte sequence
    kind           external_kind   the kind of definition being imported
    funcIndex      varuint32       the index of the exported function

    Followed by, if the kind is Function:
    kindType       varuint32       type index of the function signature

    or, if the kind is Table:
    kindType       table_type      type of the exported table

    or, if the kind is Memory:
    kindType       memory_type     type of the exported memory

    or, if the kind is Global:
    kindType       global_type     type of the exported global

    kindLen        varuint32       length of data dependent on kind type
    """
    def __init__(self, inputBytes):
        # the length of the name is the first byte
        self.exportNameLen = inputBytes[0]

        # the name is the next n bytes, where n is the length
        self.exportNameStr = inputBytes[1:1 + self.exportNameLen].decode('utf-8')

        # the kind is the next byte
        self.kind = EXTERNAL_KIND_TABLE[inputBytes[1 + self.exportNameLen]]

        # kind is one of the values found in EXTERNAL_KIND_TABLE.
        # Depending on the value of kind, the kindType maybe an integer(function kind) or an array.
        # Therefore, the length (kindLen) is dependent on the kind as well.
        # For function, because it is an integer, it will be a length of 1.
        # For the remaining kind types, the length is equal to the length of the array.
        if self.kind is 'function':
            self.kindType = inputBytes[1 + self.exportNameLen + 1]
            self.kindLen = 1

        elif self.kind is 'table':
            # TODO: create table type
            self.kindType = None
            self.kindLen = 0

        elif self.kind is 'memory':
            # TODO: create memory type
            self.kindType = None
            self.kindLen = 0

        elif self.kind is 'global':
            # TODO: create global type
            self.kindType = None
            self.kindLen = 0

        else:
            raise ValueError('Invalid kind type')

    def size(self):
        return 3 + self.exportNameLen

    def to_str(self):
        return 'ExportEntry: (export: {}, kind value: {})'.format(self.exportNameStr, self.kindType)

class GlobalEntry:
    """
    Each global_variable declares a single global variable of a given type, mutability and with the given initializer.

    Field   Type          Description
    -----------------------------------------------------
    type    global_type   type of the variables
    init    init_expr     the initial value of the global

    NOTE: in the MVP, only immutable global variables can be exported.
    """
    def __init__(self, inputBytes):
        self.type = GlobalType(inputBytes)
        self.initialExpr = InitExpr(inputBytes[self.type.size():])

    def size(self):
        return self.type.size() + self.initialExpr.size()

    def to_str(self):
        return '{}, {}'.format(self.type.to_str(), self.initialExpr.to_str())
