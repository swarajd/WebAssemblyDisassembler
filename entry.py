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

        # kind is one of the values found in EXTERNAL_KIND_TABLE.
        # Depending on the value of kind, the kind_type maybe an integer(function kind) or an array.
        # Therefore, the length (kind_len) is dependent on the kind as well.
        # For function, because it is an integer, it will be a length of 1.
        # For the remaining kind types, the length is equal to the length of the array.
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

