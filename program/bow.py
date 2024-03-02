import re

class BOW:
    def __init__(self, sentence: str, words = set()):
        sentence = re.sub(r'[^\w\s]', '', sentence).lower()

        if len(words) == 0:
            words = set(sentence.split())
        self.words = words
        
        self.bag = dict()
        for word in words:
            self.bag[word] = 0
        
        for word in sentence.split():
            self.bag[word] += 1
    
