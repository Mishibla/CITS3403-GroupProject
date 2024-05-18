test=1

random=['5', '2', '2']

norm= '1,6, 6'
rand='5,2,3,3'
yes='1,21'

noduplicate=set(norm.split(','))
#print(noduplicate)

my_string = ', '.join(f"{item}" for item in noduplicate)
#print(my_string)

print()
#wishlist_ids.add(str(ad_id))
tester=yes.split(',')
#print('2'==tester)


csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
gamesapp={'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks}
def get_rank(gametype):
    return(gamesapp.get(gametype))
def rank_id(game,rankgiven):
    ranks=gamesapp.get(game)
    list_index=ranks.index(rankgiven)
    rank_id=list_index+1
    return rank_id

print(rank_id('CSGO','SILVER'))
print(rank_id('CSGO','LEGENDARY'))