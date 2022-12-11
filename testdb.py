from ripple.core.ripple import RippleDB
import ripple.core.persist_const as persist_const

db = RippleDB(persist_const.SNAPSHOT)

#db.create("hi", "hi")
#db.create("maybe", ["call", {"not": True}])
#db.create("dima", {"age": 22, "full name": "Cambur Dmitriy", "job": "Software Engineer"})

print(db.read("hi"), db.read("maybe"), db.read("dima"))