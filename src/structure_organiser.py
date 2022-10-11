class StructureOrganiser:
    def __init__(self):
        self.tagsVector = None

    def add_tagsvector(self, tagsVector):
        self.tagsVector = tagsVector

    class TagsVector:
        def __init__(self, tags, block, inline):
            self.structure = tags
            self.block_structure = block
            self.inline_structure = inline