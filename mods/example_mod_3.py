import uno
from uno.main import *

custom_options = [
    ('First Option', (lambda quitter: print('No Beeswax'))),
    ('Second Option', (lambda quitter: print('No one expects the Spanish Inquisition'))),
    ('Third Option', (lambda quitter: quitter.__setitem__(0, True)))
]

options.insert(2, ('More', (lambda quitter: menu('Additional', custom_options))))

if __name__ == '__main__': main()