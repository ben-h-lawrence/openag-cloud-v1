import lil_db as db
uuid = '9efac8fc-432d-420c-8077-0636cbcf7f2d'

db.update('Users', **{'username':'NEWtester'}, **{'user_uuid': uuid})
