import timeit

import gifruw


TIMEIT_ROUNDS = 100
TABLE = [dict(a = 1, b = 2, c = 3, d = 4, e = 5, f = 6, g = 7, h = 8, i = 9, j = 10) for x in range(1000)]


def bigtable():
	d = gifruw.Document(autoescape_mode = False)
	with d.table():
		for row in TABLE:
			with d.tr():
				for c in row.values():
					d.td(c)
	return d.render()


if __name__ == '__main__':
	total_time = timeit.timeit(bigtable, number = TIMEIT_ROUNDS)
	print "bigtable: {:.1f} ms".format(1000 * total_time / TIMEIT_ROUNDS)

# bigtable: 18.9 ms
