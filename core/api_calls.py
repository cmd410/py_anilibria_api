import requests
import json
from functools import wraps

from .logutil import get_logger, format_api_error
from .errors import *
from .models.remote import *

host = 'https://www.anilibria.tv'

logger = get_logger(__name__)


def index_call(**kwargs):
    '''A generic call to API.
    Returns data dict.'''
    data = requests.post(host + '/public/api/index.php', data=kwargs)
    if data.status_code != 200:
        raise StatusError(f'Response status code is not 200, but {data.status_code}')
    response_data = json.loads(data.text)
    success = response_data.get('status', False)
    if not success:
        raise APIError(f'{format_api_error(response_data)}')
    return response_data


def get_releases_page(page=0, perpage=5):
    '''Get releases by page.
    Takes page number and number of releases on each page.
    Returns list of ReleaseModel'''
    response_data = index_call(query='list', page=page, perPage=perpage)
    releses = []
    for i in response_data['data']['items']:
        releses.append(ReleaseModel(i))
    return releses


def get_release(id=None, code=None):
    '''Get release by either id of code.
    Returns single ReleaseModel'''
    target = id or code
    if not target:
        raise ValueError('No id/code given')
    data = index_call(query='release', **{'id' if id else 'code': target})
    return ReleaseModel(data['data'])

def get_releases_info(id: int):
    '''Get release by id. For some reason this api call completely replicates get_release().
    Returns single ReleaseModel'''
    data = index_call(query='info', id=id)
    return ReleaseModel(data['data'][0])

def get_feed():
    data = index_call(query='feed')
    results = [determine_model(i) for i in data['data']]
    return results

def get_schedule():
    data = index_call(query='schedule')
    print(data)
    results = [TimeTableModel(i) for i in data['data']]
    return results

def get_random_release():
    return RandomReleaseModel(index_call(query='random_release')['data'])

def get_genres():
    return index_call(query='genres')['data']

def get_years():
    return index_call(query='years')['data']

def get_catalog(genre="", year="", by_popularity=False, page=0, perpage=5):
    if isinstance(genre, list):
        genre = str(genre).replace('[','').replace(']','')
    if isinstance(year, list):
        year = str(year).replace('[','').replace(']','')

    # FIXME For some reason genre/year filter does not work
    data = index_call(query='catalog',search={"genre":genre,"year":year}, sort='1' if by_popularity else '2',
                      page=page, perPage=perpage, xpage='catalog')
    return ([ReleaseModel(i) for i in data['data']['items']], PaginationModel(data['data']['pagination']))

def search_by_title(title: str):
    data = index_call(query='search', search=title)
    return [ReleaseModel(i) for i in data['data']]

def get_youtube():
    data = index_call(query='youtube')
    return ([YoutubeModel(i) for i in data['data']['items']], PaginationModel(data['data']['pagination']))

def get_vk_comments():
    data = index_call(query='vkcomments')
    return VkCommentModel(data['data'])