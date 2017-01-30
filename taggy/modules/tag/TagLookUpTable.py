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

    def __init__(self, qryObject):
        """

        :type qryObject: Queries
        """
        self.tags_lookup = []
        results = qryObject.getTags(PROVIDES_CODE)
        enumerate_tags = 0
        for row in results:
            enumerate_tags = enumerate_tags + 1
            self.tags_lookup[row['tagId']] = Tag( row['tagId'], row['tagName'], row['provideOrRequest'], enumerate_tags )

        results = qryObject.getTags(REQUEST_CODE)
        enumerate_tags = 0
        for row in results:
            enumerate_tags = enumerate_tags + 1
            self.tags_lookup[row['tagId']] = Tag( row['tagId'], row['tagName'], row['provideOrRequest'], enumerate_tags )



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


    """
    * render()
    *
    * renders in HTML a series of tags аs clickable divs
    *
    """
    def render(self):
        tags_provides = filter(self.tags_lookup, PROVIDES_CODE)

        tags_requests = filter(self.tags_lookup, REQUEST_CODE)

        print("<div id='tags'>\n")
        print("<p></p>\n")
        print("<div class='tagBtns'>")
        print("<div class='tagHeader'>PROVIDES:</div>\n")

        for t in tags_provides:
            t.render_as_div(True)

        print("<br style='clear:both' />\n")
        print("<div class='tagHeader'>REQUESTS:</div>\n")

        for t in tags_requests:
            t.render_as_div(True)

        print("<br style='clear:both' />\n")
        print("</div>\n")
        print("</div>\n")