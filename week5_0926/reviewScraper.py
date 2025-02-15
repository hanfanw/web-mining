from bs4 import BeautifulSoup
import re
import time
import requests


def run(url):
    pageNum = 2  # number of pages to collect

    fw = open('reviews.txt', 'w')  # output file

    for p in range(1, pageNum + 1):  # for each page

        print('page', p)
        html = None

        if p == 1:
            pageLink = url  # url for page 1
        else:
            pageLink = url + '?page=' + str(p) + '&sort='  # make the page url

        for i in range(5):  # try 5 times
            try:
                # use the browser to access the url
                response = requests.get(pageLink, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                html = response.content  # get the html
                break  # we got the file, break the loop
            except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
                print('failed attempt', i)
                time.sleep(2)  # wait 2 secs

        if not html:
            continue  # couldn't get the page, ignore

        soup = BeautifulSoup(html.decode('ascii', 'ignore'), 'lxml')  # parse the html

        reviews = soup.findAll('div', {'class': re.compile('review_table_row')})  # get all the review divs

        for review in reviews:

            critic, rating, source, text, date = 'NA', 'NA', 'NA', 'NA', 'NA'  # initialize

            # critic
            criticChunk = review.find('a', {'href': re.compile('/critic/')})
            if criticChunk:
                critic = criticChunk.text.strip()  # .encode('ascii','ignore')

            # rating
            ratingChunk = review.find('div', {'class': 'review_icon'})
            if ratingChunk:
                if review.find('div', {'class': 'fresh'}):
                    rating = 'fresh'
                elif review.find('div', {'class': 'rotten'}):
                    rating = 'rotten'

            # source
            sourceChunk = review.find('em', {'class': 'critic-publication'})
            if sourceChunk:
                source = sourceChunk.text.strip()

            # text of the review
            textChunk = review.find('div', {'class': 'the_review'})
            if textChunk:
                text = textChunk.text.strip()  # .encode('ascii','ignore')

            # date of the review
            dateChunk = review.find('div', {'class': 'review-date'})
            if dateChunk:
                date = dateChunk.text.strip()

            fw.write(critic + '\t' + rating + '\t' + source + '\t' + text + '\t' + date + '\n')  # write to file

    fw.close()


if __name__ == '__main__':
    url = 'https://www.rottentomatoes.com/m/space_jam/reviews/'
    run(url)
