select distinct mediacloud_story.stories_id, mediacloud_story.title, mediacloud_story.url, mediacloud_sentence.sentence
from mediacloud_story, mediacloud_sentence
where mediacloud_story.stories_id = mediacloud_sentence.stories_id and
	yearweek(mediacloud_story.publish_date, 1) = 201351
	and (mediacloud_sentence.sentence like "%RACISMO%" or
	mediacloud_sentence.sentence like "%PRECONCEITO%" or
	mediacloud_sentence.sentence like "%APARTHEID%" or
	mediacloud_sentence.sentence like "%RACIAL%" or
	mediacloud_sentence.sentence like "%SEGREGAÇÃO%" or
	mediacloud_sentence.sentence like "%SEGREGAR%");