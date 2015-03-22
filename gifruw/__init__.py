from contextlib import contextmanager
from keyword import iskeyword

from .utils import parce_ic, escape


class _ElementContextManager(object):
	
	def __init__(self, document):
		self.document = document
	
	def __enter__(self):
		document = self.document
		document._popped.append(document._pieces.pop())
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		document = self.document
		document._append(document._popped.pop())


class Document(object):
	
	# All valid HTML5 elements, according to https://developer.mozilla.org/en-US/docs/HTML/HTML5/HTML5_element_list .
	element_names = (
		{'html', 'head', 'title', 'base', 'link', 'meta', 'style'} |
		{'script', 'noscript'} |
		{'body', 'section', 'nav', 'article', 'aside', 'hgroup', 'header', 'footer', 'address', 'main'} |
		{'h' + str(n) for n in range(1, 6 + 1)} |
		{'p', 'hr', 'blockquote', 'ol', 'ul', 'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'div'} |
		{'a', 'em', 'strong', 'small', 's', 'cite', 'q', 'dfn', 'abbr', 'data', 'time', 'code', 'var', 'samp'} |
		{'kbd', 'sub', 'sup', 'i', 'b', 'u', 'mark', 'ruby', 'rt', 'rp', 'bdi', 'bdo', 'span', 'br', 'wbr'} |
		{'ins', 'del'} |
		{'img', 'iframe', 'embed', 'object', 'param', 'video', 'audio'} |
		{'source', 'track', 'canvas', 'map', 'area', 'svg', 'math'} |
		{'table', 'caption', 'colgroup', 'col', 'tbody', 'thead', 'tfoot', 'tr', 'td', 'th'} |
		{'form', 'fieldset', 'legend', 'label', 'input', 'button', 'select', 'datalist'} |
		{'optgroup', 'option', 'textarea', 'keygen', 'output', 'progress', 'meter'} |
		{'details', 'summary', 'command', 'menu'}
	)
	void_element_names = {
		'wbr', 'br', 'img', 'area', 'hr', 'param', 'keygen', 'source', 'meta',
		'command', 'base', 'track', 'link', 'embed', 'col', 'input'
	}
	
	def __init__(self, autoescape_mode = True):
		self.element_context_manager = _ElementContextManager(self)
		self._autoescape_mode = autoescape_mode
		self._pieces = []
		self._popped = []
		# Cached for performance.
		self._append = self._pieces.append
	
	@contextmanager
	def autoescape_mode(self, mode):
		old_autoescape_mode = self._autoescape_mode
		self._autoescape_mode = bool(mode)
		yield
		self._autoescape_mode = old_autoescape_mode
	
	@contextmanager
	def autoescape_off(self):
		with self.autoescape_mode(False):
			yield
	
	@contextmanager
	def autoescape_on(self):
		with self.autoescape_mode(True):
			yield
	
	def render(self):
		return u''.join(self._pieces)
	
	def __getattr__(self, name):
		
		# Elements that are also Python keywords like <del> need to be prefixed with an underscore.
		if name[0] == '_' and iskeyword(name[1:]):
			element_name = name[1:]
		else:
			element_name = name
		
		if element_name in self.element_names:
			element_func = self._get_element_func(element_name)
			# Cache the element function.
			setattr(self, name, element_func)
			return element_func
		else:
			raise AttributeError("No such element or attribute: " + name)
	
	def __iadd__(self, content):
		# Add string content without considering autoescape.
		self._append(content)
		return self
	
	def __call__(self, content):
		if self._autoescape_mode:
			content = escape(content)
		self._append(content)
	
	def doctype(self):
		self += '<!DOCTYPE html>'
	
	def _get_element_func(self, element_name):
		
		void = element_name in self.void_element_names
		_append = self._append
		if not void:
			close = '</' + element_name + '>'
		open_start = '<' + element_name
		open_end = ('/' if void else '') + '>'
		open = open_start + open_end
		
		def element(*args, **attrs):
			
			content = ""
			for arg in args:
				if isinstance(arg, basestring):
					if arg and arg[0] in '.#':
						id, classes = parce_ic(arg)
						
						if id is not None:
							attrs['id'] = id
						
						if classes:
							attrs['class'] = ' '.join(classes)
					else:
						content = arg
				else:
					content = unicode(arg)
			
			if attrs:
				attributes_string = ''
				for key, value in attrs.items():
					if not isinstance(value, basestring):
						value = unicode(value)
					attributes_string += ' ' + key.replace('_', '-') + '=\'' + escape(value).replace('\'', '&#39;') + '\''
				_append(open_start + attributes_string + open_end)
			else:
				_append(open)
			
			if self._autoescape_mode:
				content = escape(content)
			_append(content)
			
			# Return so that the with: syntax can be used.
			if not void:
				self._append(close)
				return self.element_context_manager
		return element
