import importlib
for mod in ('b001','b002','b003','b004','b005','b006','b007','b008','b009','b010','b011','b012','b013','b014','b015','b016','b017','b018','b019','b020','b021','b022','b023','b024','b025','b026','b027','finalize'):importlib.import_module(mod)
from build_cards import save,CARDS,COVER
save()
print(len(CARDS),'cards /',len(COVER),'books')
