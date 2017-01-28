
class Tag:

    tagId = 0
    name = ""
    provideOrRequest = ''
    enum = 0

    def __init__(self, tagId, name, provideOrRequest, enum=0):
        self.tagId = tagId
        self.name = name
        self.provideOrRequest = provideOrRequest
        self.enum = enum

    def __toString():
        return self.name + "_" + self.provideOrRequest

