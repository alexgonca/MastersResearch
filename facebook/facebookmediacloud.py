import ConfigParser
import MySQLdb as myDB
import requests
import time

config = ConfigParser.ConfigParser()
config.read('info.config')
con = myDB.connect(config.get('db', 'host'), config.get('db', 'username'),
                   config.get('db', 'password'), config.get('db', 'schema'))
con.set_character_set('utf8')
cur = con.cursor()
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

query = 'select stories_id, url ' \
        'from mediacloud ' \
        'where total_count is null or total_count = -1'

cur.execute(query)
urls = cur.fetchall()

for stories_id, url in urls:
    queryFacebook = "SELECT url, normalized_url, share_count, like_count, comment_count, " \
            "total_count, commentsbox_count, comments_fbid, click_count " \
            "FROM link_stat " \
            "WHERE url = \"" + url.replace('\"', "%22") + "\""

    facebook_url = "https://graph.facebook.com/fql"
    data = requests.get(facebook_url, params={'q': queryFacebook}).json()

    if data.has_key('error'):
        print '---'
        print 'Error: ' + url
        print data['error']['message']
        if data['error']['message'] == '(#4) Application request limit reached':
            print 'Delay: 10 min 30 sec'
            time.sleep(630)
            print 'Starting again!'
    else:
        cur.execute('update mediacloud '
                    'set mediacloud.facebook_url = %s, '
                    'mediacloud.normalized_url = %s, '
                    'mediacloud.share_count = %s, '
                    'mediacloud.like_count = %s, '
                    'mediacloud.comment_count = %s, '
                    'mediacloud.total_count = %s, '
                    'mediacloud.commentsbox_count = %s, '
                    'mediacloud.comments_fbid = %s, '
                    'mediacloud.click_count = %s '
                    'where mediacloud.stories_id = %s',
                    (data['data'][0]['url'], data['data'][0]['normalized_url'],
                     data['data'][0]['share_count'], data['data'][0]['like_count'], data['data'][0]['comment_count'],
                     data['data'][0]['total_count'], data['data'][0]['commentsbox_count'],
                     data['data'][0]['comments_fbid'], data['data'][0]['click_count'], stories_id))
        con.commit()