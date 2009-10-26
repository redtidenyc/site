import sgmllib

class Stripper(sgmllib.SGMLParser):
    """This strips all markup form a document
    """
    def __init__(self):
	sgmllib.SGMLParser.__init__(self)
		
    def strip(self, some_html):
        self.theString = ""
        self.feed(some_html)
        self.close()
        return self.theString
    def handle_data(self, data):
	self.theString += data

def strip_html(html):
    s = Stripper()
    return s.strip(html)
