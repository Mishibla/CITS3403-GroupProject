from app import db
from app.models import *

# Create a user instance
chris = User(username='Mishibla', name='Chris Jongue', password='securepassword')
#alec = User(username='uwu', name='Alec Wu', password='yes')
# Create ad instances and associate them with the user
ad1 = Ad(ad_id=1, ad_title='First ad on page',game_type='Valorant', game_rank='Bronze', price=20.50,skins=True, user=chris)

# Add the user and ads to the session and commit
db.session.add(chris)
#db.session.add(alec)
db.session.add(ad1)
db.session.commit()
