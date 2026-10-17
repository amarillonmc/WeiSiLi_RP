import importlib
for mod in ('b041','b042','b043','b044','b045','b046','b047','b048','b049','b050','b051','b052','b053','b054','b055','b056','b057','b058','b059','b060'):importlib.import_module(mod)
from build_cards import save,CARDS,COVER
save()
print(len(CARDS),'cards /',len(COVER),'books')
