import nltk
from nltk.util import ngrams
from nltk import word_tokenize


class Text():

    def __init__(self, text):
        self.text = text.lower()
        self.tokens = nltk.word_tokenize(self.text)
        self.pos_tags = nltk.pos_tag(self.tokens)
        self.total_number_of_tokens = len(self.tokens)
        self.row = {}
        self.build_row()

    def build_row(self):
        self.retrieve_gram_data()
        self.retrieve_pos_data()
        # self.retrieve_word_diversity_data()
        # self.retrieve_word_length_data()
        # self.retrieve_sentence_length_data()


    def retrieve_gram_data(self):
        for n in range(2, 3):
            n_grams = ngrams(self.tokens, n)
            number_of_n_grams = self.total_number_of_tokens - n + 1
            self.row.update( { n_gram : (lambda count: count / number_of_n_grams)(count) for ( n_gram, count ) in self.get_count_map(n_grams).items() } )

    def get_count_map(self, items):
        count_map = {}
        for item in items:
            if item in count_map:
                count_map[item] += 1
            else:
                count_map[item] = 1
        return count_map


    def retrieve_pos_data(self):
        for n in range(4, 5):
            pos_n_grams = []
            for i in range(0, len(self.pos_tags)+1-n):
                pos_n_grams.append( tuple([ tag for (word, tag) in  self.pos_tags[i:i+n]]) )
            self.row.update( { pos_n_gram : (lambda count: count / len(pos_n_grams))(count) for ( pos_n_gram, count ) in self.get_count_map(pos_n_grams).items() } )


def main():
    #file = open("books/oliver_twist_730.txt",'r')
    #text = Text(file.read())
    text = Text(" the beautiful cat sits. the beautiful cat sits ")
    text.build_row()
    print(text.row)


if __name__ == '__main__':
    main()
