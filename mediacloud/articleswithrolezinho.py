# -*- coding: utf-8 -*-
import mediacloud
import ConfigParser
import MySQLdb as myDB

config = ConfigParser.ConfigParser()
config.read('info.config')

mc = mediacloud.api.MediaCloud(config.get('api','key'))
con = myDB.connect(config.get('db','host'), config.get('db','username'),
                   config.get('db','password'), config.get('db','schema'))

with con:
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    stopIteration = False
    lastProcessed_stories_id = 0

    while not stopIteration:
        storiesWithRolezinho = mc.storyList(u'( +(rolesinhos OR rolesinho OR rolêsinhos OR rolêsinho OR rolezinhos '
                                            u'OR rolezinho OR rolêzinhos OR rolêzinho OR rolês OR rolê OR rolé OR '
                                            u'rolés OR rolézinho OR rolézinhos OR rolésinho OR rolésinhos) AND '
                                            u'+publish_date:[2013-12-07T00:00:00Z TO 2014-05-04T23:59:59Z] ) OR '
                                            u'( +shopping AND +itaquera AND '
                                            u'+publish_date:[2013-12-07T00:00:00Z TO 2013-12-15T23:59:59Z] )',
                                            u'+(tags_id_media:8877968 OR tags_id_media:8875452 OR '
                                            u'tags_id_media:8878226)', lastProcessed_stories_id, 1000)
        if len(storiesWithRolezinho) == 0:
            stopIteration = True
        else:
            print "============================"
            print "More records: " + str(len(storiesWithRolezinho))
            print "============================"
            for story in storiesWithRolezinho:
                print story['processed_stories_id']
                cur.execute('INSERT INTO mediacloud_story '
                            '(full_text_rss, media_id, description, language, url, title, processed_stories_id,'
                            'publish_date, guid, db_row_last_updated, is_fully_extracted, stories_id, collect_date,'
                            'story_text)'
                            'values (%s, %s, %s, %s, %s, %s, %s, str_to_date(%s, \'%%Y-%%m-%%d %%H:%%i:%%s\'),'
                            '%s, str_to_date(%s, \'%%Y-%%m-%%d %%H:%%i:%%s\'), %s, %s,'
                            'str_to_date(%s, \'%%Y-%%m-%%d %%H:%%i:%%s\'), %s)',
                            (story['full_text_rss'], story['media_id'], story['description'],
                             story['language'], story['url'], story['title'], story['processed_stories_id'],
                             story['publish_date'], story['guid'], story['db_row_last_updated'][:19],
                             story['is_fully_extracted'], story['stories_id'],
                             story['collect_date'], story['story_text']))
                lastProcessed_stories_id = story['processed_stories_id']
                if 'story_sentences' in story.keys():
                    for sentence in story['story_sentences']:
                        print '...' + str(sentence['sentence_number'])
                        cur.execute("INSERT into mediacloud_sentence "
                                    "(story_sentences_id, sentence, sentence_number, stories_id) "
                                    "values (%s, %s, %s, %s)",
                                    ( sentence['story_sentences_id'], sentence['sentence'], sentence['sentence_number'],
                                      sentence['stories_id']))