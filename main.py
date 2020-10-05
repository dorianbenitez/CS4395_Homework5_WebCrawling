import pickle
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
        if "login" not in link.get('href') and "getnewsmart" not in link.get(
                'href') and "centralbanking" not in link.get('href') and len(link.get('href')) > 5:
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
            raw = f.read().replace('\\n', '').replace('\\t', '').replace('\\r', '')
        count += 1

        sent_tokens = nltk.sent_tokenize(raw)
        with open(str(count) + ".txt", 'w') as f:
            for t in range(len(sent_tokens)):
                if '\\' not in sent_tokens[t]:
                    f.write(str(sent_tokens[t].encode("utf-8")) + '\n')

    count = 16  # this is temporary, delete after uncommenting part 2

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
    for i in range(0, 40):
        if next(iter(sort_orders[i])) != "b":
            print("\t" + str(i + 1) + ". " + next(iter(sort_orders[i])))

    # 5.    Manually determine the top 10 terms from step 4, based on your domain knowledge.
    dk_10_list = ["home", "buy", "sell", "rates", "marketplace", "new", "insights", "property", "area", "information"]

    # 6. Build a searchable knowledge base of facts that a chatbot (to be developed later) can share related to the 10 terms.
    # The “knowledge base” can be as simple as a Python dict which you can pickle.
    # More points for something more sophisticated like sql.
    knowledge_base = "Hello, my name is ChatBot.\n" \
                     "A homeowners net worth is over thirty times greater than that of a renter.\n" \
                     "61.4% of the average American familys net worth is in home equity.\n" \
                     "The average mortgage interest rate in the United States is 3.21%.\n" \
                     "North Carolina is leading the United States in millennial population.\n" \
                     "The best day of the week to list your home for sale is on a Friday.\n" \
                     "On average, 500 people move to Atlanta, Georgia every day\n" \
                     "Dallas, Texas has the highest employment rate in the United States.\n" \
                     "The median sale price of a home is $328,419 in the United States.\n" \
                     "In 2019, number of homes sold was 652,878 in the United States.\n" \
                     "In 2019, the number of American homes that went up for sale was 1,066,903.\n" \
                     "The number of American homes newly listed on the market is 691,785.\n" \
                     "The number of homes sold above their original listing is 32%.\n" \
                     "The three most competetive cities in the U.S. housing market are Tacoma, WA, Grand Rapids, MI, and Spokane, WA.\n" \
                     "The three fastest growing metropolitan cities in the U.S. housing market are Cleveland, OH, Memphis, TN, and Toms River, NJ.\n" \
                     "A large amount of people are relocating from California to Texas within the past couple of years.\n" \
                     "Houston, Texas is the fourth largest city in the United States by population.\n" \
                     "52.9% of Dallas, Texas residents are renters vs. the national average of 33%.\n" \
                     "In 2017, investors owned/rented out about 18.2 million one-unit homes, including detached homes, townhomes, and duplexes, providing housing for about 42 percent of the nation’s 43 million renter households.\n" \
                     "Rental properties more often than not guarantee a steady rate on your investment.\n" \
                     "The two most important benefits of owning rental properties is generating cash flow and value from appreciation.\n" \
                     "In 2019, there were about 14.7 million households and 45.2 million residents renting single-family homes in the United States.\n" \
                     "In 2013, NAR reported that the median age of first-time buyers was 31. On average these buyers purchased a 1,670 square-foot home costing $170,000.\n" \
                     "The nationwide nominal house price index is now 40% above its 2012 low-point and 4% above the peak reached in 2006.\n" \
                     "The mountain region has the highest house price increases year after year.\n" \
                     "Residential construction activity continues to rise strongly, partly driven by lower mortgages rates.\n" \
                     "According to a NAR Community Preference Survey, 78% of respondents said that the neighborhood is more important to them than the size of the home.\n" \
                     "The most affordable zip codes with the best schools in the U.S. are 64014, 46060, and 75023.\n" \
                     "The worst time to buy a home is when inventory is running low, meaning that prices are high.\n" \
                     "According to the U.S. Census Bureau, the average person will move 12 times within their lifetime.\n" \
                     "80% of people aged 65 and older own their own homes.\n" \
                     "The number of people renting homes aged over 59, grew 43% in the last 10 years."
    kb_sents = sent_tokenize(knowledge_base)

    with open('KnowledgeBase.txt', 'w') as f:
        for i in range(len(kb_sents)):
            f.write(str(kb_sents[i]) + '\n')

    dict_counter = 1

    kb_dict = {}
    for sentence in kb_sents:
        kb_dict.update({sentence: dict_counter})
        dict_counter += 1
    pickle.dump(kb_dict, open("KnowledgeBasePickle", 'wb'))

    # 7.    In a doc: (1) describe how you created your knowledge base,
    # include screen shots of the knowledge base, and indicate your top 10 terms;
    # (2) write up a sample dialog you would like to create with a chatbot based on your knowledge base
