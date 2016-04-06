import random

class Markov(object):

    def __init__(self, open_file):
        self.cache = {}
        self.open_file = open_file
        self.words = self.file_to_words()
        self.word_size = len(self.words)
        self.database()

    def file_to_words(self):
        self.open_file.seek(0)
        data = self.open_file.read()
        words = data.split()
        return words

    def doubles(self):
        if len(self.words) < 2:
            return

        for i in range(len(self.words) - 1):
            yield (self.words[i], self.words[i+1])

    def database(self):
        for w1, w2 in self.doubles():
            key = w1
            if key in self.cache:
                self.cache[key].append(w2)
            else:
                self.cache[key] = [w2]

    def generate_text(self, size=25):
        seed = random.randint(0, self.word_size - 2)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in range(size):
            gen_words.append(w1)
            try:
                w1, w2 = w2, random.choice(self.cache[w2])
            except KeyError:
                break
        gen_words.append(w2)
        return ' '.join(gen_words)
