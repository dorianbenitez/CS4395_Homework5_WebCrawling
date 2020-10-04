import sys
import re
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from urllib import request
import urllib.request
import nltk

# function to determine if an element is visible
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


# Main function
if __name__ == '__main__':
    # 1.    Build  a web crawler function that starts with a URL representing a topic and outputs a list of at least 15
    # relevant URLs. The URLs can be pages within the original domain but should have a few outside the original domain
    starter_url = "https://www.wsj.com/news"
    r = requests.get(starter_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    url_list = []

    counter = 0
    print("\nRelevant URLs: ")

    # Print all the URLs and append each to a list
    for link in soup.find_all('a'):
        if "login" not in link.get('href') and "getnewsmart" not in link.get('href') and "centralbanking" not in link.get('href') and len(link.get('href')) > 5:
            url_list.append((str(link.get('href'))))
            print("\t" + str(counter + 1) + ". " + link.get('href'))
            counter += 1
        if counter > 39:
            break


    # 2.    Write a function to loop through your URLs and scrape all text off each page.
    #       Store each page’s text in its own file
    url_text = []
    count = 0

    # for i in range(len(url_list)):
    #     try:
    #         html = urllib.request.urlopen(url_list[i])
    #     except:
    #         pass
    #     soup = BeautifulSoup(html, "html.parser")
    #     data = soup.findAll(text=True)
    #     result = filter(visible, data)
    #     temp_list = list(result)  # list from filter
    #     temp_str = ' '.join(temp_list)
    #     if len(temp_str) > 1500 and count < 15 and "javascript" not in temp_str.lower() and "unsupported browser" not in temp_str.lower():
    #         count += 1
    #         with open(str(count) + ".txt", 'w') as f:
    #             f.write(str(temp_str.encode("utf-8")))
    #     if count == 15:
    #         break

    # 3.    Write a function to clean up the text. You might need to delete newlines and tabs.
    # Extract sentences with NLTK’s sentence tokenizer.
    # Write the sentences for each file to a new file. That is, if you have 15 files in, you have 15 files out.
    for i in range(1, 16):
        with open(str(i) + ".txt", 'r') as f:
            raw = f.read().replace('\\n', '').replace('\\t', ''). replace('\\r', '')
        count += 1

        sent_tokens = nltk.sent_tokenize(raw)
        with open(str(count) + ".txt", 'w') as f:
            for t in range(len(sent_tokens)):
                if '\\' not in sent_tokens[t]:
                    f.write(str(sent_tokens[t].encode("utf-8")) + '\n')


    count = 16 # this is temporary, delete after uncommenting part 2

    # 4.    Write a function to extract at least 25 important terms from the pages using an importance measure such as
    # term frequency, or tf-idf. First, it’s a good idea to lower-case everything, remove stopwords and punctuation.
    # Print the top 25-40 terms.
    tf_dict = {}

    for i in range(16, 30):
        with open(str(count) + ".txt", 'r') as f:
            lower_raw = f.read().lower()
        tokens = word_tokenize(lower_raw)
        tokens = [w for w in tokens if w.isalpha()
                  and w not in stopwords.words('english')]
        for t in tokens:
            if t in tf_dict:
                tf_dict[t] += 1
            else:
                tf_dict[t] = 1

        for t in tf_dict.keys():
            tf_dict[t] = tf_dict[t] / len(tokens)
        count += 1

    sort_orders = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    print("\nMost important words: ")
    for i in range(0,30):
        if next(iter(sort_orders[i])) != "b":
            print("\t" + str(i+1) + ". " + next(iter(sort_orders[i])))




    # 5.    Manually determine the top 10 terms from step 4, based on your domain knowledge.

    # 6.    Build a searchable knowledge base of facts that a chatbot (to be developed later) can share related to the 10 terms.
    # The “knowledge base” can be as simple as a Python dict which you can pickle.
    # More points for something more sophisticated like sql.

    # 7.    In a doc: (1) describe how you created your knowledge base,
    # include screen shots of the knowledge base, and indicate your top 10 terms;
    # (2) write up a sample dialog you would like to create with a chatbot based on your knowledge base