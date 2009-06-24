import sys, os, codecs, types


try:
	import encodings.utf_32
	has_utf32 = True
except:
	has_utf32 = False

class ConfigInputStream(object):
	"""
	An input stream which can read either ANSI files with default encoding
	or Unicode files with BOMs.

	Handles UTF-8, UTF-16LE, UTF-16BE. Could handle UTF-32 if Python had
	built-in support.
	"""
	def __init__(self, stream):
		"""
		Initialize an instance.

		@param stream: The underlying stream to be read. Should be seekable.
		@type stream: A stream (file-like object).
		"""
		encoding = None
		signature = stream.read(4)
		used = -1
		if has_utf32:
			if signature == codecs.BOM_UTF32_LE:
				encoding = 'utf-32le'
			elif signature == codecs.BOM_UTF32_BE:
				encoding = 'utf-32be'
		if encoding is None:
			if signature[:3] == codecs.BOM_UTF8:
				used = 3
				encoding = 'utf-8'
			elif signature[:2] == codecs.BOM_UTF16_LE:
				used = 2
				encoding = 'utf-16le'
			elif signature[:2] == codecs.BOM_UTF16_BE:
				used = 2
				encoding = 'utf-16be'
			else:
				used = 0
		if used >= 0:
			stream.seek(used)
		if encoding:
			reader = codecs.getreader(encoding)
			stream = reader(stream)
		self.stream = stream
		self.encoding = encoding

	def read(self, size):
		if (size == 0) or (self.encoding is None):
			rv = self.stream.read(size)
		else:
			rv = u''
			while size > 0:
				rv += self.stream.read(1)
				size -= 1
		return rv

	def close(self):
		self.stream.close()

	def readline(self):
		if self.encoding is None:
			line = ''
		else:
			line = u''
		while True:
			c = self.stream.read(1)
			if c:
				line += c
			if c == '\n':
				break
		return line


WORD = 'a'
NUMBER = '9'
STRING = '"'
EOF = ''
LCURLY = '{'
RCURLY = '}'
LBRACK = '['
LBRACK2 = 'a['
RBRACK = ']'
COMMA = ','
COLON = ':'
MINUS = '-'
TRUE = 'True'
FALSE = 'False'
NONE = 'None'

WORDCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_"

if sys.platform == 'win32':
	NEWLINE = '\r\n'
elif os.name == 'mac':
	NEWLINE = '\r'
else:
	NEWLINE = '\n'

class ConfigError(Exception):
	"""
	This is the base class of exceptions raised by this module.
	"""
	pass

class ConfigFormatError(ConfigError):
	"""
	This is the base class of exceptions raised due to syntax errors in
	configurations.
	"""
	pass

class ConfigReader(object):
	"""
	This internal class implements a parser for configurations.

	>>> conf = Holder()
	>>> cr = ConfigReader(conf)
	>>> cr.load("webber.conf")
	>>> print conf.lang
	de
	>>> import cStringIO
	>>> s = cStringIO.StringIO("num: 1\\nlang: 'us'")
	>>> cr.load(s)
	>>> print conf.lang
	us
	>>> print conf.num
	1
	>>> s = cStringIO.StringIO("arr: [1,2]")
	>>> cr.load(s)
	>>> print conf.arr
	[1, 2]
	>>> s = cStringIO.StringIO("assoc: {a:11, b:22}")
	>>> cr.load(s)
	>>> print conf.assoc["a"], conf.assoc["b"]
	11 22
	"""

	def __init__(self, config):
		self.filename = None
		self.config = config
		self.lineno = 0
		self.colno = 0
		self.lastc = None
		self.last_token = None
		self.whitespace = ' \t\r\n'
		self.quotes = '\'"'
		self.punct = ':-+*/%,.{}[]()@`$'
		self.digits = '0123456789'
		self.wordchars = '%s' % WORDCHARS # make a copy
		self.identchars = self.wordchars + self.digits
		self.pbchars = []
		self.pbtokens = []

	def location(self):
		"""
		Return the current location (filename, line, column) in the stream
		as a string.

		Used when printing error messages,

		@return: A string representing a location in the stream being read.
		@rtype: str
		"""
		return "%s(%d,%d)" % (self.filename, self.lineno, self.colno)

	def getChar(self):
		"""
		Get the next char from the stream. Update line and column numbers
		appropriately.

		@return: The next character from the stream.
		@rtype: str
		"""
		if self.pbchars:
			c = self.pbchars.pop()
		else:
			c = self.stream.read(1)
			self.colno += 1
			if c == '\n':
				self.lineno += 1
				self.colno = 1
		return c

	def __repr__(self):
		return "<ConfigReader at 0x%08x>" % id(self)

	__str__ = __repr__

	def getToken(self):
		"""
		Get a token from the stream. String values are returned in a form
		where you need to eval() the returned value to get the actual
		string. The return value is (token_type, token_value).

		Multiline string tokenizing is thanks to David Janes (BlogMatrix)

		@return: The next token.
		@rtype: A token tuple.
		"""
		if self.pbtokens:
			return self.pbtokens.pop()
		stream = self.stream
		token = ''
		tt = EOF
		while True:
			c = self.getChar()
			if not c:
				break
			if c in self.quotes:
				token = c
				quote = c
				tt = STRING
				escaped = False
				multiline = False
				c1 = self.getChar()
				if c1 == quote:
					c2 = self.getChar()
					if c2 == quote:
						multiline = True
						token += quote
						token += quote
					else:
						self.pbchars.append(c2)
						self.pbchars.append(c1)
				else:
					self.pbchars.append(c1)
				while True:
					c = self.getChar()
					if not c:
						break
					token += c
					if (c == quote) and not escaped:
						if not multiline or (len(token) >= 6 and token.endswith(token[:3]) and token[-4] != '\\'):
							break
					if c == '\\':
						escaped = not escaped
					else:
						escaped = False
				if not c:
					raise ConfigFormatError('%s: Unterminated quoted string: %r, %r' % (self.location(), token, c))
				break
			if c in self.whitespace:
				self.lastc = c
				continue
			elif c in self.punct:
				token = c
				tt = c
				if (self.lastc == ']') or (self.lastc in self.identchars):
					if c == '[':
						tt = LBRACK2
				break
			elif c in self.digits:
				token = c
				tt = NUMBER
				while True:
					c = self.getChar()
					if not c:
						break
					if c in self.digits:
						token += c
					elif (c == '.') and token.find('.') < 0:
						token += c
					else:
						if c and (c not in self.whitespace):
							self.pbchars.append(c)
						break
				break
			elif c in self.wordchars:
				token = c
				tt = WORD
				c = self.getChar()
				while c and (c in self.identchars):
					token += c
					c = self.getChar()
				if c: # and c not in self.whitespace:
					self.pbchars.append(c)
				if token == "True":
					tt = TRUE
				elif token == "False":
					tt = FALSE
				elif token == "None":
					tt = NONE
				break
			else:
				raise ConfigFormatError('%s: Unexpected character: %r' % (self.location(), c))
		if token:
			self.lastc = token[-1]
		else:
			self.lastc = None
		self.last_token = tt
		return (tt, token)

	def load(self, stream):
		"""
		Load the configuration from the specified stream.

		@param stream: A stream from which to load the configuration.
		@type stream: A stream (file-like object).
		@param suffix: The suffix of this configuration in the parent
		configuration. Should be specified whenever the parent is not None.
		@raise ConfigError: If parent is specified but suffix is not.
		@raise ConfigFormatError: If there are syntax errors in the stream.
		"""

		if type(stream) == types.StringType:
			stream = ConfigInputStream(file(stream, 'rb'))

		self.setStream(stream)
		self.token = self.getToken()
		self.parseMappingBody(self.config)
		if self.token[0] != EOF:
			raise ConfigFormatError('%s: expecting EOF, found %r' % (self.location(), self.token[1]))

	def setStream(self, stream):
		"""
		Set the stream to the specified value, and prepare to read from it.

		@param stream: A stream from which to load the configuration.
		@type stream: A stream (file-like object).
		"""
		self.stream = stream
		if hasattr(stream, 'name'):
			filename = stream.name
		else:
			filename = '?'
		self.filename = filename
		self.lineno = 1
		self.colno = 1

	def match(self, t):
		"""
		Ensure that the current token type matches the specified value, and
		advance to the next token.

		@param t: The token type to match.
		@type t: A valid token type.
		@return: The token which was last read from the stream before this
		function is called.
		@rtype: a token tuple - see L{getToken}.
		@raise ConfigFormatError: If the token does not match what's expected.
		"""
		if self.token[0] != t:
			raise ConfigFormatError("%s: expecting %s, found %r" % (self.location(), t, self.token[1]))
		rv = self.token
		self.token = self.getToken()
		return rv

	def parseMappingBody(self, parent):
		"""
		Parse the internals of a mapping, and add entries to the provided
		L{Mapping}.

		@param parent: The mapping to add entries to.
		@type parent: A L{Mapping} instance.
		"""
		while self.token[0] in [WORD, STRING]:
			self.parseKeyValuePair(parent)

	def parseKeyValuePair(self, parent):
		"""
		Parse a key-value pair, and add it to the provided L{Mapping}.

		@param parent: The mapping to add entries to.
		@type parent: A L{Mapping} instance.
		@raise ConfigFormatError: if a syntax error is found.
		"""
		tt, tv = self.token
		if tt == WORD:
			key = tv
			suffix = tv
		elif tt == STRING:
			key = eval(tv)
			suffix = '[%s]' % tv
		else:
			msg = "%s: expecting word or string, found %r"
			raise ConfigFormatError(msg % (self.location(), tv))
		self.token = self.getToken()
		# for now, we allow key on its own as a short form of key : True
		if self.token[0] == COLON:
			self.token = self.getToken()
			value = self.parseValue(parent, suffix)
		else:
			value = True
		try:
			parent[key] = value
		except Exception, e:
			raise ConfigFormatError("%s: %s, %r" % (self.location(), e,
									self.token[1]))
		tt = self.token[0]
		if tt not in [EOF, WORD, STRING, RCURLY, COMMA]:
			msg = "%s: expecting one of EOF, WORD, STRING, RCURLY, COMMA, found %r"
			raise ConfigFormatError(msg  % (self.location(), self.token[1]))
		if tt == COMMA:
			self.token = self.getToken()

	def parseValue(self, parent, suffix):
		"""
		Parse a value.

		@param parent: The container to which the value will be added.
		@type parent: A L{Container} instance.
		@param suffix: The suffix for the value.
		@type suffix: str
		@return: The value
		@rtype: any
		@raise ConfigFormatError: if a syntax error is found.
		"""
		tt = self.token[0]
		if tt in [STRING, WORD, NUMBER, TRUE, FALSE, NONE, MINUS]:
			rv = self.parseScalar()
		elif tt == LBRACK:
			rv = self.parseSequence(parent, suffix)
		elif tt in [LCURLY]:
			rv = self.parseMapping(parent, suffix)
		else:
			raise ConfigFormatError("%s: unexpected input: %r" % (self.location(), self.token[1]))
		return rv

	def parseSequence(self, parent, suffix):
		"""
		Parse a sequence.

		@param parent: The container to which the sequence will be added.
		@type parent: A L{Container} instance.
		@param suffix: The suffix for the value.
		@type suffix: str
		@return: a L{Sequence} instance representing the sequence.
		@rtype: L{Sequence}
		@raise ConfigFormatError: if a syntax error is found.
		"""
		rv = []
		self.match(LBRACK)
		tt = self.token[0]
		while tt in [STRING, WORD, NUMBER, LCURLY, LBRACK, TRUE, FALSE, NONE]:
			suffix = '[%d]' % len(rv)
			value = self.parseValue(parent, suffix)
			rv.append(value)
			tt = self.token[0]
			if tt == COMMA:
				self.match(COMMA)
				tt = self.token[0]
				continue
		self.match(RBRACK)
		return rv

	def parseMapping(self, parent, suffix):
		"""
		Parse a mapping.

		@param parent: The container to which the mapping will be added.
		@type parent: A L{Container} instance.
		@param suffix: The suffix for the value.
		@type suffix: str
		@return: a L{Mapping} instance representing the mapping.
		@rtype: L{Mapping}
		@raise ConfigFormatError: if a syntax error is found.
		"""
		if self.token[0] == LCURLY:
			self.match(LCURLY)
			rv = {}
			self.parseMappingBody(rv)
			self.match(RCURLY)
		return rv

	def parseScalar(self):
		"""
		Parse a scalar - a terminal value such as a string or number, or
		an L{Expression} or L{Reference}.

		@return: the parsed scalar
		@rtype: any scalar
		@raise ConfigFormatError: if a syntax error is found.
		"""
		tt = self.token[0]
		if tt in [NUMBER, WORD, STRING, TRUE, FALSE, NONE]:
			rv = self.token[1]
			if tt != WORD:
				rv = eval(rv)
			self.match(tt)
		elif tt == MINUS:
			self.match(MINUS)
			rv = -self.parseScalar()
		else:
			raise ConfigFormatError("%s: unexpected input: %r" %
			   (self.location(), self.token[1]))
		#print "parseScalar: '%s'" % rv
		return rv



class Holder(object):
	"""This is a simple wrapper class so that you can write

	h = Holder(bar=1, baz="test")

	instead of writing

	foo["bar"] = 1
	baz["bar"] = "test"

	Holder will be the base class for all configurations and objects.
	"""

	def __init__(self, **kw):
		"""Creates a new folder object:

		>>> h = Holder(bar=1, baz="test")
		>>> print h.bar
		1
		>>> print h.baz
		test
		"""
		self.__dict__.update(kw)
		self._inherit_from = []

	def keys(self):
		"""Return list of stored variables.

		>>> h = Holder(bar=1, baz="test")
		>>> print sorted(h.keys())
		['bar', 'baz']
		"""
		return filter(lambda x: x[0] != '_', self.__dict__.keys())

	def has_key(self, key):
		return self.__dict__.has_key(key)

	def setDefault(self, key, value):
		if not self.__dict__.has_key(key):
			self.__dict__[key] = value

	def __getitem__(self, key):
		"""Allows access to the variables via obj[name] syntax.

		>>> h = Holder()
		>>> h.foo = "Hello"
		>>> print h["foo"]
		Hello
		"""
		try:
			return self.__dict__[key]
		except:
			pass
		for inh in self._inherit_from:
			try:
				return inh[key]
			except:
				pass
		raise KeyError(key)

	__getattr__ = __getitem__

	def __setitem__(self,key,val):
		"""Allows access to the variables via obj[name] syntax.

		>>> h = Holder()
		>>> h["foo"] = "Hello"
		>>> print h.foo
		Hello
		"""
		self.__dict__[key] = val

	def inheritFrom(self, holder):
		"""
		This allows on Holder to inherit settings from another holder.

		>>> h1 = Holder(a=1, b=2)
		>>> h2 = Holder(c=3)
		>>> h2.inheritFrom(h1)
		>>> print h2.c
		3
		>>> print h2["b"]
		2
		>>> print h2.a
		1
		"""
		self._inherit_from.append(holder)

	def load(self, stream):
		"""
		>>> conf = Holder()
		>>> cr = ConfigReader(conf)
		>>> cr.load("webber.conf")
		>>> print conf.lang
		de
		"""
		cr = ConfigReader(self)
		cr.load(stream)

	def __repr__(self):
		return "<%s object: " % self.__class__.__name__ + ",".join(self.keys()) + ">"





def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
