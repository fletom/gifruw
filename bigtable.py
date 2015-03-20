import timeit

import gifruw


TIMEIT_ROUNDS = 50
TABLE = [dict(a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8, i = 9, j = 10) for x in range(1000)]


def bigtable():
	d = gifruw.Document(autoescape_mode = False)
	with d.table():
		for row in TABLE:
			with d.tr():
				for c in row.values():
					# This would be the normal syntax:
					d.td(c)
	return d.render()


def bigtable_optimized():
	d = gifruw.Document(autoescape_mode = False)
	with d.table():
		for row in TABLE:
			with d.tr():
				for c in row.values():
					# However, if you actually wanted to do something 10k times,
					# you'd optimize it like this:
					d += '<td>%s</td>' % c
	return d.render()


for f in [bigtable, bigtable_optimized]:
	total_time = timeit.timeit(f, number = TIMEIT_ROUNDS)
	print "{}: {:.1f} ms".format(f.__name__, 1000 * total_time / TIMEIT_ROUNDS)

# bigtable: 61.5 ms
# bigtable_optimized: 14.4 ms
