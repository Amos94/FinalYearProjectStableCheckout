from taggy.modules.Queries import Queries
from taggy.modules.tag.Tag import Tag

PROVIDES_CODE = 'P'
REQUEST_CODE = 'R'

class TagLook:

    """
    * represents the tags_lookup table as a map of tagIds->Tag classes
    *
    * @var array
    """
    tags_lookup = []

    """
    * constructor to gets an associated array of tags indexed by their
    * tag ID (i.e. a tag lookup table)
    *
    * @param Queries $qryObject a DB Queries object
    * @return array an assoc. array of Tag objected indexed by their id as int
    """

    def __init__(self):
        """

        :type qryObject: Queries
        """
        qryObject = Queries()
        self.tags_lookup = []
        results = qryObject.getTags(PROVIDES_CODE)
        enumerate_tags = 0
        for row in results:
            enumerate_tags = enumerate_tags + 1
            #tagId = 0
            #tagName = 1
            #provideOrRequest = 3
            self.tags_lookup.insert(row[0], Tag( row[0], row[1], row[3], enumerate_tags ))

        results = qryObject.getTags(REQUEST_CODE)
        enumerate_tags = 0
        for row in results:
            enumerate_tags = enumerate_tags + 1
            self.tags_lookup.insert(row[0], Tag( row[0], row[1], row[3], enumerate_tags ))



    """
    * tag()
    *
    * looks up Tag object by tagID
    *
    * @param string $tagID
    * @return Tag object
    """
    def tag(self, tagId):
        return self.tags_lookup[tagId]


    def render(self):
        toReturn = ''
        tags_provides = filter(lambda k:PROVIDES_CODE in self.tags_lookup, self.tags_lookup)

        tags_requests = filter(lambda k:REQUEST_CODE in self.tags_lookup, self.tags_lookup)

        toReturn += "<div id='tags'><br>"
        toReturn += "<p></p><br>"
        toReturn += "<div class='tagBtns'>"
        toReturn += "<div class='tagHeader'>PROVIDES:</div><br>"

        for t in tags_provides:
            t.render_as_div(True)

        toReturn += "<br style='clear:both' /><br>"
        toReturn += "<div class='tagHeader'>REQUESTS:</div><br>"

        for t in tags_requests:
            t.render_as_div(True)

        toReturn += "<br style='clear:both' /><br>"
        toReturn += "</div><br>"
        toReturn += "</div><br>"
        return toReturn