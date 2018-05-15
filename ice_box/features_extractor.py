import pandas as pd
import os
from text_features import Text
import random

def build_df(author, max_ngrams):
    books_df = pd.DataFrame()

    path = "./data/texts_cleaned/" + author
    books = os.listdir(path)
    if '.DS_Store' in books:
        books.remove('.DS_Store')

    #random sample of books
    # num = 15
    # random_int = random.sample(range(0,len(books)), num)
    # for i in random_int:

    for i in range(0, len(books)):
        if books[i] == '.DS_Store':
            continue
        book_path = path + "/" + books[i]
        with open(book_path, encoding="utf8", errors='ignore') as f:
            contents = f.read()
        text = Text(contents, author, max_ngrams) #text, author, number of ngrams
        row = pd.DataFrame( text.row, index = [books[i]] )
        books_df = books_df.append(row)
        #print(books_df.shape,": ",books[i])

    books_df = books_df.fillna(0)
    return books_df
    #return process(books_df, 0.15, 0.85) #lower level author preprocess

def process(books_df, lower_bound, upper_bound):
    std = books_df.std(numeric_only=True)
    std = std.sort_values()
    not_ngrams = ['word_length_std_dev','word_length_avg','sentence_length_std_dev','word_richness','sentence_length_avg','number_sentences']
    std.drop(not_ngrams, axis=0, inplace=True)
    # for n in not_ngrams:
    #     del std[n]
    lower = std.quantile(q=lower_bound)
    upper = std.quantile(q=upper_bound)
    del_col = std[std <= lower].append( std[std >= upper])
    keys = del_col.keys()
    books_df.drop(keys, axis=1, inplace=True)
    print(books_df.shape)
    return books_df


def combine_author_df(authors):
    author_dfs = []
    for author in authors:
        print(author)
        author_df = build_df(author ,3)
        author_dfs.append(author_df)
    books_df = pd.concat(author_dfs)
    books_df = books_df.fillna(0)
    print(books_df.shape)
    books_df.to_csv("2author_pos_3grams.csv", sep='\t', encoding='utf-8')


def main():
    #authors = ['oscar_wilde','mildred_a._wirt','mark_twain']
    authors = ['oscar_wilde','mildred_a._wirt']

    combine_author_df(authors)
    books_df = pd.read_csv('./2author_pos_3grams.csv', sep='\t')
    process_df = process(books_df, 0.25, 0.75)
    process_df.to_csv("2author_pos_3grams_processed.csv", sep='\t', encoding='utf-8')


if __name__ == "__main__":
    main()