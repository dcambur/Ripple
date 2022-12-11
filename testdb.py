from ripple.core.ripple import RippleDB
import ripple.core.persist_const as persist_const

db = RippleDB(persist_const.AOF)
db.read("hi")
dct = db.read("nested")

print(dct)