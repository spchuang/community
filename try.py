from app import db
from app.models import User, Community, user_community

FILTER_BY_USER = True
user = User().query.filter_by(user_name='spchuang').first()




subq_members = db.session.query(
                  (user_community.c.community_id).label('id'),
                  db.func.count(user_community.c.user_id).label('num_members')
               )\
               .group_by(user_community.c.community_id)\
               .subquery()

subq_is_member = db.session.query(
                  (user_community.c.community_id).label('id'),
                  db.func.count(user_community.c.user_id).label('is_member')
               )\
               .filter(user_community.c.user_id==user.id)\
               .group_by(user_community.c.community_id)\
               .subquery()

#return number of members in each group and whether the user is a member
query = db.session.query(
            Community,
            subq_members.c.num_members,
            subq_is_member.c.is_member
         )\
         .join(user_community)\
         .filter(user_community.c.community_id == Community.id, user_community.c.user_id==user.id)\
         .outerjoin(subq_members, subq_members.c.id == Community.id)\
         .outerjoin(subq_is_member, subq_is_member.c.id == Community.id)\
         .group_by(Community)

print User().query.filter_by(id=1).first().joined_communities.all()



print "RESULT"
print query.all()
for c in query.all():
    print c.keys()
    print c.num_members
    print c[0]
    print c[2]

