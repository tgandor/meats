select id, text, (select max(outprint_date) from outprints where label_id=l.id) as last_printed
from labels l
order by last_printed desc;
