# number of stories per week
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where active and
	mediacloud.stories_id = mediacloud_sentence.stories_id
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# frame arrastao
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%ARRASTÃO%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# frame apartheid
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%RACISMO%" or
	mediacloud_sentence.sentence like "%PRECONCEITO%" or
	mediacloud_sentence.sentence like "%APARTHEID%" or
	mediacloud_sentence.sentence like "%RACIAL%" or
	mediacloud_sentence.sentence like "%SEGREGAÇÃO%" or
	mediacloud_sentence.sentence like "%SEGREGAR%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%LIMINAR%") and active
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# week #2
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%FUNK%" or
	mediacloud_sentence.sentence like "%MC %" or
	mediacloud_sentence.sentence like "%OSTENTAÇÃO%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# week #3
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%CONSUMO%" or
	mediacloud_sentence.sentence like "%CONSUMIR%" or
	mediacloud_sentence.sentence like "%CONSUMISMO%" or
	mediacloud_sentence.sentence like "%CLASSE MÉDIA%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# week #6
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%MANIFESTAÇÃO%" or
	mediacloud_sentence.sentence like "%MANIFESTAÇÕES%" or
	mediacloud_sentence.sentence like "%PROTESTO%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# week #6
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%COPA%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%MORTE%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%DIREITO%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%VIOLÊNCIA%" or
	mediacloud_sentence.sentence like "%VIOLENT%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

# week #12
select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%STF%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);


select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%APARTHEID%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);

select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%PARQUE%" and
	mediacloud_sentence.sentence like "%ROLEZINHO%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);


select yearweek(mediacloud.publish_date, 1), count(distinct mediacloud_sentence.stories_id)
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	(mediacloud_sentence.sentence like "%LIMINAR%")
group by yearweek(mediacloud.publish_date, 1)
order by yearweek(mediacloud.publish_date, 1);