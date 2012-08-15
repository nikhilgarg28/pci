from sets import Set
from pydelicious import get_popular, get_userposts, get_urlposts

# Returns a set of users who recently posted a
# popular link with tag = tag. count is a lose measure of how many users are
# chosen
def initializeUserDict(tag, count=5):
    users = Set()
    #get the top count popular posts
    for post in get_popular(tag=tag)[:count]:
        #Find all urls which refer to this post
        for post_alias in get_urlposts(post['url']):
            user = post_alias['user']
            users.add(user)
    return users

#Sanity check
#print initializeUserDict('Programming')

def fill_urls(users):
    user_urls = {}
    all_urls = Set()
    for user in users:
        user_urls[user] = {}
        #We'll make 3 attempts at finding out posts of this user
        for trial in xrange(3):
            try:
                #Let's get recent posts made by this user
                posts = get_userposts(user)
                break
            except:
                print 'Failed to fetch posts of the user %s' %user
        for post in posts:
            url = post['url']
            user_urls[user][url] = 1
            all_urls.add(url)

    #We need to ensure that all users have all the urls as features. Those who
    #din't post a url would've its value as 0
    for user in users:
        for url in all_urls:
            if url not in user_urls[user]:
                user_urls[user][url] = 0
    return user_urls

# Sanity check 2
users = initializeUserDict(tag = 'Quora')
print fill_urls(users)
