import feedparser
import re
from collections import defaultdict
import os
from sets import Set

# Returns the title and dictionary of word counts for an RSS feed
def get_word_counts(url):
    print 'processing', url
    #Parse the feed
    parsed_feed = feedparser.parse(url)
    word_count = defaultdict(int)

    # Loop over all the entries
    for e in parsed_feed.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

        # Extract a list of words from the summary
        words = get_words(e.title + ' ' + summary)
        for word in words:
            word_count[word] += 1

    title = parsed_feed.feed.title if 'title' in parsed_feed.feed else url
    return title, word_count

# Returns a list of all words in this html page
def get_words(html):
    # Remove all HTML tags firstly
    text = re.compile(r'<[^>]+>').sub('', html)

    # Split words by all non-alpha characters
    words = re.compile(r'[^A-Za-z]+').split(text)

    # Convert to lower case
    return [word.lower() for word in words if len(word) > 0]

# Reads a feedurls.txt and for each url in file, generates its wordcounts
def generate_word_count_file(feedurl_file = '../data/feedlist.txt',
                             outfile = '../data/blogdata.txt'):

    #presence_count[w] contains the count of blogs that contain this word
    presence_count = defaultdict(int)
    word_counts = {}

    feedurl_path = os.path.normpath(os.path.join(os.getcwd(), feedurl_file))
    num_of_blogs = 0

    for feedurl in open(feedurl_path):
        num_of_blogs += 1
        title, wc = get_word_counts(feedurl)
        word_counts[title] = wc

        for word in wc:
            presence_count[word] += 1

    # All words scanned so far aren't valid. we should try to remove common
    # words (like 'the', 'is' etc) and also we should try to remove those words
    # which appear in a very small number of blogs

    valid_words = Set()
    for w, pc in presence_count.items():
        frac = float(pc) / num_of_blogs
        if frac > 0.1 and frac < 0.5:
            valid_words.add(w)

    # Now let's write everything down as a matrix to the outfile
    outfile_path = os.path.normpath(os.path.join(os.getcwd(), outfile))

    # Words might be unicode strings, best to use codecs
    import codecs
    with codecs.open(outfile_path, 'w', encoding='utf-8') as out:
        out = open(outfile_path, 'w')
        out.write('Blog')
        for word in valid_words:
            out.write('\t%s' % word)
        out.write('\n')

        for blog, blog_wc in word_counts.items():
            try:
                out.write(blog)
            except:
                out.write('dummy')

            for word in valid_words:
                count = blog_wc[word] if word in blog_wc else 0
                out.write('\t%d' % count)
            out.write('\n')



# Let'see if everything so far works
generate_word_count_file()
