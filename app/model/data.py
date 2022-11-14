
import datetime


class Data(object):
    def __init__(self, id=None, url:str = None, title: str = None, date_added: datetime = None):
        self.id = id
        self.url = url
        self.title = title
        self.date_added = date_added   


    def to_json(self):
        if isinstance(self.date_added,datetime.datetime):
            self.date_added = str(self.date_added)
        return {"id": self.id, "url": self.url, "title":self.title, "date_added": self.date_added}

