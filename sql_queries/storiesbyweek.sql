select distinct date(publish_date), stories_id, eliminate_quotes(title), url
from mediacloud_story
where yearweek(mediacloud_story.publish_date, 1) = 201351
order by mediacloud_story.publish_date;