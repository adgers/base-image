from lxml import etree
import copy, re

class xtree(object):
	def __init__(self, input_file):
		self.input_file = input_file
		self.is_valid = False
		self.tree = None
		self.errors = None
		self.escape_entities = False
	
	def parse(self, dtd_validation=True, encode_entities=True):
		parser = etree.XMLParser(dtd_validation=dtd_validation,
								 resolve_entities=False,
								 remove_comments=True)
		try:
			#if escape_ents:
			#	doc = etree.fromstring(self.encode_entities(), parser)
			#	self.tree = etree.ElementTree(doc)	
			if encode_entities:
				self.escape_entities=True
				clean_pat = re.compile('&([^&;]*;)')		
				with open(self.input_file) as f:
					doc = etree.fromstring(clean_pat.sub(r'##\1', f.read()), parser)
					self.tree = etree.ElementTree(doc)	
			else:
				self.tree = etree.parse(self.input_file, parser)
			self.is_valid = True

		except etree.XMLSyntaxError, e:
			self.errors = e
		
	def serialise(self, output_file, decode_entities=True):
		if decode_entities and self.escape_entities:
			decode_pat = re.compile('##([^&;]*;)')
			with open(output_file, 'w') as f:
				return f.write(decode_pat.sub(r'&\1', etree.tostring(self.tree)))
		self.tree.write(output_file)
		
	def	insert_node(self, parent, text, node, before=False):
		node.tail = ''
		if before:
			node.tail = text		
		r = parent.xpath("*|text()|processing-instruction()")
		l = self.__findtext(r, text, node, before)
		self.__chainNode(l, parent)

	def wrap_text(self, parent, text, element):
		if(element.text is None):
			element.text = text
		else:
			element.text= text + element.text
		element.tail = ''
		r = parent.xpath("*|text()|processing-instruction()")
		l = self.__findtext(r,text,element, True)
		self.__chainNode(l,parent)
			
	def __chainNode(self, nodelist, node):
		""" chain the tokens of nodelist together to the node
			clear the node at first
			if the first token is string, it become the node.text
			if the token is obj(element or pi) and it followed by a string 
				move the string as the token.tail
			append the obj to the node
			result: the node got updated
		"""
		if(len(nodelist)<1): return None
		
		for nd in node.getchildren():
			node.remove(nd)
		node.text=''
		# remove the heading string tokens
		i=0
		while (i<len(nodelist) and isinstance(nodelist[i], str)):
			node.text = node.text+nodelist[i]
			nodelist.remove(nodelist[i])
			
		while (i<len(nodelist)):
			if(not isinstance(nodelist[i],str)):
				if(i<(len(nodelist)-1) and isinstance(nodelist[i+1], str)):
					# put the following sting as tail
					nodelist[i].tail = nodelist[i].tail + nodelist[i+1]
					nodelist.remove(nodelist[i+1])
				else:
					# add the obj and move to next item
					node.append(copy.deepcopy(nodelist[i]))
					i=i+1
		

	def __findtext(self, nodelist, text, node, before=False):
		""" 
			Insert node before or after specified text.
			Nodelist represents the children of the current node.
			
		"""
		width = len(text)
		L=[]
		for item in nodelist:
			n=0 # index of a string to the found keyword
			st=0 # search start point
			if(not isinstance(item, str)):
				# if it's not string add it to L and move on
				item.tail=''
				L.append(copy.deepcopy(item))
			else:
				while (n<len(item) and n!=-1):
					n=item.lower().find(text.lower(),st)
						
					if (n==-1):	
						# not found add last part of the string
						L.append(item[st:])
					else:
						if (n>0):
							# add 1st part of the string
							L.append(item[st:n])
						if(not before):
							L.append(text)
						L.append(copy.deepcopy(node))
						# set the st at the end of the found text
						st=n+width

		return copy.deepcopy(L)

		
