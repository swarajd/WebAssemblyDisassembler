from type import EXTERNAL_KIND_TABLE

class ImportEntry:
    def __init__(self, inputBytes):
        """
        field       type            description
        ---------------------------------------------------------
        module_len  varuint32       length of module_str in bytes
        module_str  bytes           module name: valid UTF-8 byte sequence
        field_len   varuint32       length of field_str in bytes
        field_str   bytes           field name: valid UTF-8 byte sequence
        kind        external_kind   the kind of definition being imported

        Followed by, if the kind is Function:
        kind_type        varuint32       type index of the function signature

        or, if the kind is Table:
        kind_type        table_type      type of the imported table

        or, if the kind is Memory:
        kind_type        memory_type     type of the imported memory

        or, if the kind is Global:
        kind_type        global_type     type of the imported global
        """
        self.module_len = inputBytes[0]
        self.module_str = inputBytes[1:1 + self.module_len].decode('utf-8')

        self.field_len = inputBytes[1 + self.module_len]
        field_str_index = 2 + self.module_len
        self.field_str = inputBytes[field_str_index:field_str_index + self.field_len].decode('utf-8')

        self.kind = EXTERNAL_KIND_TABLE[inputBytes[field_str_index + self.field_len]]

        if self.kind is 'function':
            self.kind_type = inputBytes[field_str_index + self.field_len + 1]
            self.kind_len = 1

        elif self.kind is 'table':
            # TODO: create table type
            self.kind_type = None
            self.kind_len = 0

        elif self.kind is 'memory':
            # TODO: create memory type
            self.kind_type = None
            self.kind_len = 0

        elif self.kind is 'global':
            # TODO: create global type
            self.kind_type = None
            self.kind_len = 0

        else:
            raise ValueError('Invalid kind type')

    def size(self):
        return 3 + self.module_len + self.field_len + self.kind_len

    def to_str(self):
        return 'ImportEntry: (module: {}, field: {}, kind_value: {})'.format(self.module_str, self.field_str, self.kind_type)

class ExportEntry:
    """
    field          type            description
    ---------------------------------------------------------
    exportNameLen  varuint32       length of module_str in bytes
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

    kindLen        
    """
    def __init__(self, inputBytes):
        # the length of the name is the first byte
        self.exportNameLen = inputBytes[0]

        # the name is the next n bytes, where n is the length
        self.exportNameStr = inputBytes[1:1 + self.exportNameLen].decode('utf-8')

        # the kind is the next byte
        self.kind = EXTERNAL_KIND_TABLE[inputBytes[1 + self.exportNameLen]]

        # parse the kind
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
        return 3 + self.exportNameLen + self.kindLen

    def to_str(self):
        return 'ImportEntry: (export: {}, kind value: {})'.format(self.exportNameStr, self.kindType)
        