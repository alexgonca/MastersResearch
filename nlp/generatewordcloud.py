# -*- coding: utf-8 -*
import ConfigParser
from nltk.corpus import PlaintextCorpusReader
import nltk
import uuid
import MySQLdb as myDB
import string
from nltk import bigrams
from nltk import trigrams

def generate_word_frequency(label, initial_date, final_date, include_repeats=True, include_complete_text=False,
                            search_terms=['ROLÊ', 'ROLÉ', 'ROLESINHO', 'ROLEZINHO']):
    print label

    # connect to the database
    config = ConfigParser.ConfigParser()
    config.read('info.config')
    con = myDB.connect(config.get('db', 'host'), config.get('db', 'username'),
                       config.get('db', 'password'), config.get('db', 'schema'))
    con.set_character_set('utf8')
    cur = con.cursor()
    cur.execute('SET NAMES utf8;')
    cur.execute('SET CHARACTER SET utf8;')
    cur.execute('SET character_set_connection=utf8;')

    # create corpus text file according to the parameters
    if include_repeats:
        query = 'select sentence '
    else:
        query = 'select distinct eliminate_quotes(sentence) '
    query += 'from mediacloud, mediacloud_sentence ' \
             'where active and date(mediacloud.publish_date) >= "' + initial_date +\
             '" and date(mediacloud.publish_date) <= "' + final_date +\
             '" and mediacloud.stories_id = mediacloud_sentence.stories_id '
    if not include_complete_text:
        query += 'and ('
        for index in range(0, len(search_terms)):
            query += "upper(sentence) like \"%" + search_terms[index] + '%"'
            if index != len(search_terms)-1:
                query += " or "
            else:
                query += ") "
    query += 'order by mediacloud.stories_id, sentence_number '
    filename = str(uuid.uuid4())
    query += 'INTO OUTFILE "/tmp/' + filename + '" CHARACTER SET utf8'
    print query
    cur.execute(query)

    # calculate frequency distribution of the words in the specified corpus.
    corpus = PlaintextCorpusReader("/tmp", filename, encoding='utf-8')
    words = nltk.wordpunct_tokenize(corpus.raw())
    content = []
    for w in words:
        remove_punctuation_map = dict((ord(char), None) for char in (string.punctuation + u"”“–·’—‘»"))
        word = w.lower().translate(remove_punctuation_map)
        if word == u'':
            word = u'###'
        if len(word) == 1:
            word = u'###'
        if word.isdigit():
            word = u'###'
        content = content + [word]

    frequency_distribution_unigrams = nltk.FreqDist(content)
    frequency_distribution_bigrams  = nltk.FreqDist(bigrams(content))
    frequency_distribution_trigrams = nltk.FreqDist(trigrams(content))

    cur.execute('delete from wordfrequency_query where label = "' + label + '"')

    cur.execute("SELECT word, max_grams FROM stopword")
    stopwords_aux = cur.fetchall()
    stopwords = dict((word.decode('utf8'), grams) for word, grams in stopwords_aux)

    # save the frequency distribution in the database
    cur.execute('INSERT INTO wordfrequency_query '
                '(label, initial_date, final_date, include_repeats, include_complete_text)'
                'values (%s, %s, %s, %s, %s)',
                (label, initial_date, final_date, include_repeats, include_complete_text))

    for unigram in frequency_distribution_unigrams.keys():
        if frequency_distribution_unigrams[unigram] != 1 and unigram not in stopwords.keys():
            cur.execute('INSERT INTO wordfrequency '
                        '(label, word, frequency)'
                        'values (%s, %s, %s)',
                        (label, unigram, str(frequency_distribution_unigrams[unigram])))

    for bigram in list(frequency_distribution_bigrams.keys()):
        insert = True
        if frequency_distribution_bigrams[bigram] == 1:
            insert = False
        else:
            if bigram[0] in stopwords.keys():
                if stopwords[bigram[0]] >= 2:
                    insert = False
            if bigram[1] in stopwords.keys():
                if stopwords[bigram[1]] >= 2:
                    insert = False
            if bigram[0] + u" " + bigram[1] in stopwords.keys():
                if stopwords[bigram[0] + u" " + bigram[1]] >= 2:
                    insert = False
        if insert:
            cur.execute('INSERT INTO wordfrequency '
                        '(label, word, frequency)'
                        'values (%s, %s, %s)',
                        (label, bigram[0] + u" " + bigram[1], str(frequency_distribution_bigrams[bigram])))

    for trigram in list(frequency_distribution_trigrams.keys()):
        insert = True
        if frequency_distribution_trigrams[trigram] == 1:
            insert = False
        else:
            if trigram[0] in stopwords.keys():
                if stopwords[trigram[0]] >= 3:
                    insert = False
            if trigram[1] in stopwords.keys():
                if stopwords[trigram[1]] >= 3:
                    insert = False
            if trigram[2] in stopwords.keys():
                if stopwords[trigram[2]] >= 3:
                    insert = False
            if trigram[0] + u" " + trigram[1] in stopwords.keys():
                if stopwords[trigram[0] + u" " + trigram[1]] >= 3:
                    insert = False
            if trigram[1] + u" " + trigram[2] in stopwords.keys():
                if stopwords[trigram[1] + u" " + trigram[2]] >= 3:
                    insert = False
            if trigram[0] + u" " + trigram[1] + u" " + trigram[2] in stopwords.keys():
                if stopwords[trigram[0] + u" " + trigram[1] + u" " + trigram[2]] >= 3:
                    insert = False
        if insert:
            cur.execute('INSERT INTO wordfrequency '
                        '(label, word, frequency)'
                        'values (%s, %s, %s)',
                        (label, trigram[0] + u" " + trigram[1] + u" " + trigram[2],
                         str(frequency_distribution_trigrams[trigram])))

    con.commit()

generate_word_frequency('liminar', '2014-01-06', '2014-01-12', include_repeats=False,
                        include_complete_text=False)
#generate_word_frequency('week-02', '2013-12-16', '2013-12-22', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-03', '2013-12-23', '2013-12-29', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-04', '2013-12-30', '2014-01-05', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-05', '2014-01-06', '2014-01-12', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-06', '2014-01-13', '2014-01-19', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-07', '2014-01-20', '2014-01-26', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-08', '2014-01-27', '2014-02-02', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-09', '2014-02-03', '2014-02-09', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-10', '2014-02-10', '2014-02-16', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-11', '2014-02-17', '2014-02-23', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-12', '2014-02-24', '2014-03-02', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-13', '2014-03-03', '2014-03-09', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-14', '2014-03-10', '2014-03-16', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-15', '2014-03-17', '2014-03-23', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-16', '2014-03-24', '2014-03-30', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-17', '2014-03-31', '2014-04-06', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-18', '2014-04-07', '2014-04-13', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-19', '2014-04-14', '2014-04-20', include_repeats=False, include_complete_text=False)
#generate_word_frequency('week-20', '2014-04-21', '2014-04-27', include_repeats=False, include_complete_text=False)
