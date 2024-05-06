from app import db
from app.models import *

Chris = User(
    username='Mishibla',
    name='Chris Jongue',
    password='database',
    ad_id=1
)

ad1 = Ad(
    ad_id=1,
    ad_title='First ad on page',
    user_name='Mishibla'
)

db.session.add_all([Chris, ad1])
db.session.commit()