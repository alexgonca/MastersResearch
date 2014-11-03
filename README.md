Master's Research
=================

During my Master's, I studied computer-assisted framing analysis. My thesis is [available online](http://casadecachorro.com.br/alex/thesis.pdf). I used a recent controversy in Brazilian media (the *rolezinhos*: flashmobs organized by low-income youth in Brazilian shopping malls) to test the methods I developed in my research.

In this repository, you can find all source code generated during my research. The code is organized in folders that are described as follows.

## mediacloud

My research largely relied on [Media Cloud](http://www.mediacloud.org) data. In fact, I helped to [localize Media Cloud](https://github.com/alexgonca/MediaCloudLocalization) to the Brazilian media ecosystem. The folder [mediacloud](mediacloud) has the Python code for creating the corpus used in my research (all stories that mention the word "rolezinho" or associated terms). It was implemented with the [MediaCloud Python API](https://github.com/c4fcm/MediaCloud-API-Client).

## google

In order to enrich my corpus and avoid blind spots in my data set, I added links obtained from searches in Google with the same keywords used in my Media Cloud query ("rolezinho" and variations). Google prevents automation of searches and after a few requests it shuts down the requester's IP. Nonetheless, I found a way of using [Selenium](http://www.seleniumhq.org/) to implement the web scraping of the Google searches.

## mysql

All data was stored in a MySQL database. This folder contains the script that creates the tables. It also contains some queries used to analyse the data.

## facebook

My corpus was comprised by about 4,000 articles. It would be unfeasible to submit each one of them to content analysis. Therefore, it was important to identify the stories that had the highest impact in public opinion. But how can one do that? I used facebook data. In concrete, the data about the statistics related to links shared on the social network and available through the facebook query language. The assumption was that the articles that generated the highest numbers of likes, shares, and comments were presumably the ones with highest impact in shaping public opinion.

## nlp
