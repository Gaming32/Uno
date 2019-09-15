import uno
p1 = uno.Player()
w = uno.NetworkWrapper('localhost', p1)
w.poll_event()