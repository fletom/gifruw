# gifruw

gifruw is an experimental templating engine for Python. The templates themselves are nothing but pure Python code.

It uses the "with" syntax and context managers that were introduced in Python 2.5 with [PEP 343](http://www.python.org/dev/peps/pep-0343/). It therefore takes advantage of Python's self-enforcing whitespace-significant structure, which is nice if you're into that sort of thing.

## Design

Firstly, it's designed to be small, extendable, and customizable. It's essentially just one class that you can easily subclass to suit your needs.

One caveat is that it's not intended to include large blocks of text inline. These can only be done using Python triple-quoted strings and it doesn't look that nice. Instead, you should render text from a "content" file using a markup language like Markdown and put that inside your XScribe templates.

An advantage it has over most other templating languages is that it's much less prone to the (in my experience) extremely common errors and typos you normally get when writing HTML. You'll never have extra/mismatched closing or opening tags that can mess up the rest of the page or cause subtle bugs. You'll never have indentation that confusingly doesn't match the actual structure of the document. In fact, as far as I can tell it's only capable of producing syntactically valid HTML, meaning you only have to worry about semantics.

## Example

This example demonstrates instantiating a `gifruw.Document`, and rendering a standard HTML page with a stylesheet and a few `<div>`s, as well as using the "selector" class and ID syntax and the HTML data attribute syntax.

```
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
```


## Performance

It's fast enough.