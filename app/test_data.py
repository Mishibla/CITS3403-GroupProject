from app import db
from app.models import *

# Create a user instance
chris = User(username='Mishibla', name='Chris Jongue', password='securepassword')

# Create ad instances and associate them with the user
ad1 = Ad(ad_id=1, ad_title='First ad on page', user=chris)
ad2 = Ad(ad_id=2, ad_title='Second ad on page', user=chris)


# Add the user and ads to the session and commit
db.session.add(chris)
db.session.add(ad1)
db.session.add(ad2)
db.session.commit()
