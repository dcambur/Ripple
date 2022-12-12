from ripple.core.ripple import RippleDB
from ripple.core.transaction import Transaction
import ripple.core.persist_const as persist_const

db = RippleDB(persist_const.NONE)

with Transaction(db) as trans:
    trans.add("hi", "hi")
    trans.add("maybe", ["call", {"not": True}])
    trans.add("dima", {"age": 22, "full name": "Cambur Dmitriy", "job": "Software Engineer"})

# db.create("hi", "hi")
# db.create("maybe", ["call", {"not": True}])
# db.create("dima", {"age": 22, "full name": "Cambur Dmitriy", "job": "Software Engineer"})

print(db.read("hi"), db.read("maybe"), db.read("dima"))
