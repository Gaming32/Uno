import uno
p1 = uno.Player()
w = uno.NetworkWrapper('localhost', p1)
w.poll_events_forever()
o = w.other
p = o.play
# uno.time.sleep(120)
# print(o.play)
print(o.play(uno.YELLOW_3))