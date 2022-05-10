cip = "由由工 工井 工井 由由王 由中人 由田田 由由由 由由田 由由王 羊大 由由中 羊夫 由由羊 由由田 羊大 由中由 由由由 由由夫 由由工 羊大 由田井 由田大 由田中 由田由 由中大"

dh = '田由中人工大王夫井羊'
ds = '0123456789'

s = ''
for i in cip:
	if i in dh:
		s += ds[dh.index(i)]
	else:
		s += ' '

dlist = s.split(" ")
res = ''
for i in dlist:
	res += chr(int(i))

print(res)
