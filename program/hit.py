import pickle

class Hit:
    def __init__(self, params_dict):
        self.title = params_dict.get('title', None)
        self.venue = params_dict.get('venue', None)
        self.pages = params_dict.get('pages', None)
        self.year = params_dict.get('year', None)
        self.type = params_dict.get('type', None)
        self.access = params_dict.get('access', None)
        self.doi = params_dict.get('doi', None)

    def get_from_file(file_name):
        with open(file_name, 'rb') as file:
            hits = pickle.load(file)
            return hits
    
    def __str__(self):
        return f'{self.year} {self.title}'
    
    
def hit_to_dict(hit):
        return {
            "title": hit.title,
            "venue": hit.venue,
            "pages": hit.pages,
            "year": hit.year,
            "type": hit.type,
            "access": hit.access,
            "doi": hit.doi
        }