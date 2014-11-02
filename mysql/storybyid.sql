select sentence
from mediacloud, mediacloud_sentence
where mediacloud.stories_id = mediacloud_sentence.stories_id and
	mediacloud.stories_id = '185901614'
order by sentence_number;