import gifruw


def index():
	d = gifruw.Document()
	d.doctype()
	with d.html():
		with d.head():
			d.link(rel = 'stylesheet', type = 'text/css', href = 'style.css')
		
		with d.body():
			with d.div('#header'):
				d.h1('Welcome')
			
			with d.div('#content'):
				d.a(
					"My great website.",
					href = 'http://example.com',
					data_myattr = 'HTML data- attributes!'
				)
			
			with d.div('#footer'):
				d.p('#spam.my_class.stuff', "What a nice footer!")
	
	return d.render()


table = [dict(a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8, i = 9, j = 10) for x in range(1000)]

def bigtable():
	d = gifruw.Document()
	with d.autoescape_off():
		with d.table():
			for row in table:
				with d.tr():
					for c in row.values():
						# If you actually wanted to do something 10k times,
						# you'd optimize it like this:
						d += '<td>' + str(c) + '</td>'
	
	return d.render()

# In [1]: %timeit bigtable()
# 10 loops, best of 3: 19.1 ms per loop
