
def clean_path(path: str):
    while path.startswith('/'):
        path = path[1:]
    if '..' in path:
        path = path.replace('..', '')
        while '//' in path:
            path = path.replace('//', '/')
    return path

