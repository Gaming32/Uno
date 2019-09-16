import uno
p1 = uno.Player()
p = uno.NetworkPlayer(p1)
o = p.other
print(p.play(uno.BLUE_5))
o.poll_events()