from ripple.core.ripple import RippleDB
import ripple.core.persist_const as persist_const

db = RippleDB(persist_const.AOF)
dt = db.read("me")
dt2 = db.read("call")
print(dt[0], dt2)
