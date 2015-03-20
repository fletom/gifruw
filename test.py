import nose
from nose.tools import *

import gifruw


def test_basic_html():
	d = gifruw.Document()
	d.doctype()
	with d.html():
		with d.body():
			d.p('test')
	
	assert_equal(d.render(),
		'<!DOCTYPE html>'
		'<html>'
			'<body>'
				'<p>test</p>'
			'</body>'
		'</html>'
	)


def test_autoescape():
	d = gifruw.Document()
	d.p("&<>")
	with d.autoescape_off():
		d.p("&<>")
	
	assert_equal(d.render(), '<p>&amp;&lt;&gt;</p><p>&<></p>')


def test_ic():
	d = gifruw.Document()
	d.div('#id.class1.class2')
	
	assert_equal(d.render(), '<div id=\'id\' class=\'class1 class2\'></div>')


def test_attributes():
	d = gifruw.Document()
	d.h1('Header', style = 'bar')
	d.div(data_attr = 'foo')
	
	assert_equal(d.render(), '<h1 style=\'bar\'>Header</h1><div data-attr=\'foo\'></div>')


def test_void_element():
	d = gifruw.Document()
	d.img(src = 'image')
	
	assert_equal(d.render(), '<img src=\'image\'/>')


if __name__ == '__main__':
	nose.main()
