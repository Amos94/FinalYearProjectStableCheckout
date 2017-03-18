PROVIDES_CODE = 'P'
REQUEST_CODE = 'R'
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

    def toString(self):
        return self.name + "_" + self.provideOrRequest

    def render_in_table(self):
        print("[" + self.name + "(" + self.provideOrRequest+ ")]")

    def render_as_div(self, is_tagBtn = False, is_editable = True ):

        # CODE TO BE REVIEWED BECAUSE OF STRANGE ? "" :


        if(is_tagBtn):
            kind = 'tagBtn'
        else:
            kind = 'tagInstance'

        tag_enumerated_class = "tag" + self.enum
        tag_provideOrRequest_class = "tag"+ self.provideOrRequest
        tag_enumerated_provideOrRequest_class = "tag"+ self.provideOrRequest+ self.enum

        print("<div id='t"+ self.tagID+"' class='tag "+ kind+" "+is_editable +" "+tag_enumerated_class+" "+tag_provideOrRequest_class+" "+tag_enumerated_provideOrRequest_class+" '>")

    def is_provides(self):
        return self.provideOrRequest == PROVIDES_CODE

    def is_request(self):
        return self.provideOrRequest == REQUEST_CODE