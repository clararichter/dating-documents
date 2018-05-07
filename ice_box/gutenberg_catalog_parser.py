import csv
import re

def parse_catalog():
    outfile = open('./gutenberg_catalog.csv','w')
    writer = csv.DictWriter(outfile, fieldnames=['title', 'author', 'book_id'])

    content = open("gutenberg_original_catalog.txt").read()
    content = re.sub(' +',' ', content)
    content = content.replace(u'\xa0', u' ')
    content = re.sub(r'\[#[0-9]+\]*\[.*\]', '', content)


    pattern1 = r'\n[A-Za-z0-9 ,.\'\"()-:?&$]+, by [A-Za-zëéèòó .-,]+ [0-9]+'
    pattern2 = r'\n[A-Za-z0-9 ,.\'\"()-:?&$]+ [0-9]+\n[A-Za-z0-9 ,.\'\"()-:&$]+, by [A-Za-zëéèòó .-,]+'


    works = re.findall(pattern1, content)
    for w in works:
        # print(w)
        title = re.search('.+(?=, by)', w)
        author_and_id = re.search('(?<=, by ).+', w)
        author = re.search('.+(?= [0-9]+)', author_and_id[0])
        book_id = re.search('[0-9]+', author_and_id[0])

        # print("TITLE: ", title[0])
        # print("AUTHOR: ", author[0])
        # print("ID: ", book_id[0])
        # writer.writerow( {"title": title[0], "author": author[0], "book_id" : book_id[0]} )

    content = re.sub(pattern1, '', content)

    works = re.findall(pattern2, content)
    for w in works:
        # print(w)
        book_id = re.search( r'[0-9]+(?=\n)', w )
        w = w.replace('\n', ' ')

        author = re.search('(?<=, by )[A-Za-z .-]+', w)

        title = re.search('.+(?=, by)', w)
        title = re.sub(r' (\d+) ', '', title[0])
        # print("TITLE: ", title)
        # print("AUTHOR: ", author[0])
        # print("ID: ", repr(book_id[0]))

        # writer.writerow( {"title": title, "author": author[0], "book_id" : book_id[0]} )

    content = re.sub(pattern2, '', content)
    print(content)


parse_catalog()