def to_db_str(str):
    return str.replace(' ', '_').lower()


def to_view_str(str):
    return str.replace('_', ' ').title()


def to_search_str(str):
    return str.replace(' ', '').replace('-', '').replace('_', '').lower()


def image_url_handler(url):
    idx = url.find('/static/')
    return url[idx:]
