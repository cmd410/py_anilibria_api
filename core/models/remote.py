import json

from ..logutil import get_logger

logger = get_logger(__name__)

def determine_model(d: dict):
    '''Returns Model object for given dict, or returns dict if can`t determine model.'''
    subs = RemoteModel.__subclasses__()
    keys = set(d.keys())
    for cls in subs:
        needed_keys = set(cls.json_fields)
        needed_keys ^= keys
        if len(needed_keys) <= 3:
            return cls(d)
    return d

def is_all_dict(l):
    for i in l:
        if not isinstance(i, dict):
            return False
    return True

def is_all_model(l):
    if not isinstance(l, list):
        return False
    for i in l:
        if not isinstance(i, RemoteModel):
            return False
    return True

class RemoteModel:
    json_fields = {}

    def __str__(self):
        data = {}
        for field in self.json_fields:
            if not hasattr(self, field):
                if hasattr(self, field.lower()):
                    field = field.lower()
                else:
                    continue
            value = getattr(self, field)
            data[field] = value
        return str(data)

    def __init__(self, d):
        self.from_dict(d)

    def from_dict(self, d: dict):
        for field in self.json_fields:
            value = d.get(field) or d.get(field.lower())
            if not hasattr(self, field):
                if hasattr(self, field.lower()):
                    field = field.lower()
                else:
                    continue
            if isinstance(value, dict):
                value = determine_model(value)
            elif isinstance(value, list):
                if is_all_dict(value):
                    new_list = []
                    for i in value:
                        model = determine_model(i)
                        if isinstance(model, dict):
                            continue
                        new_list.append(model)
                    value = new_list
            elif isinstance(value, str):
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '').isdigit():
                    value = float(value)
            setattr(self, field, value)


class ReleaseModel(RemoteModel):
    json_fields = {"id" ,"code", "names", "series", "poster", "favorite", "last", "moon", "status", "type",
                    "genres", "voices", "year", "day", "description", "blockedInfo", "playlist", "torrents"}
    def __init__(self, d):
        self.id = 0
        self.code = ''
        self.names = []
        self.series = 0
        self.poster = ''
        self.favorite = ''
        self.last = 0
        self.moon = 0
        self.status = ''
        self.type = ''
        self.genres = []
        self.voices = []
        self.year = 0
        self.day = 0
        self.description = ''
        self.blockinfo = None
        self.playlist = []
        self.torrents = []

        super().__init__(d)


class RandomReleaseModel(RemoteModel):
    json_fields = {"code"}

    def __init__(self, d):
        self.code = 0
        super().__init__(d)

class SeriesModel(RemoteModel):
    json_fields = {"id", "title", "sd", "hd", "fullhd", "srcSd", "srcHd"}

    def __init__(self,d):
        self.id = 0
        self.title = ''
        self.sd = ''
        self.hd = ''
        self.fullhd = ''
        self.srcsd = ''
        self.srchd = ''
        super().__init__(d)


class TorrentModel(RemoteModel):
    json_fields = {'id', 'hash', 'leechers', 'seeders', 'completed', 'quality', 'series', 'size', 'url', 'ctime'}

    def __init__(self, d):
        self.id = 0
        self.hash = 0
        self.leechers = 0
        self.seeders = 0
        self.completed = 0
        self.quality = ''
        self.series = ''
        self.size = 0
        self.url = ''
        self.ctime = 0

        super().__init__(d)

class BlockedModel(RemoteModel):
    json_fields = {"blocked", "reason"}

    def __init__(self, d):
        self.blocked = False
        self.reason = ''
        super().__init__(d)

class FavoriteModel(RemoteModel):
    json_fields = {"rating", "added"}

    def __init__(self, d):
        self.rating = 0
        self.added = False
        super().__init__(d)

class FeedModel(RemoteModel):
    json_fields = {"release", "youtube"}

    def __init__(self, d):
        self.release = None
        self.youtube = None

        super().__init__(d)


class TimeTableModel(RemoteModel):
    json_fields = {"day", "items"}

    def __init__(self, d):
        self.day = 1
        self.items = []

        super().__init__(d)


class UserModel(RemoteModel):
    json_fields = {"id", "login", "avatar"}

    def __init__(self, d):
        self.id = 0
        self.login = ''
        self.avatar = ''

        super().__init__(d)


class YoutubeModel(RemoteModel):
    json_fields = {"id", "title", "image", "vid", "views", "comments", "timestamp"}

    def __init__(self, d):
        self.id = 0
        self.title = ''
        self.image = ''
        self.vid = ''
        self.views = 0
        self.comments = 0
        self.timestamp = 0

        super().__init__(d)

class VkCommentModel(RemoteModel):
    json_fields = {"baseUrl", "script"}

    def __init__(self, d):
        self.baseurl = ''
        self.script = ''
        super().__init__(d)


class PaginationModel(ReleaseModel):
    json_fields = {"page","perPage","allPages","allItems"}

    def __init__(self, d):
        self.page = 0
        self.perpage = 0
        self.allpages = 0
        self.allitems = 0
        super().__init__(d)