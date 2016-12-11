# import sys
# sys.path.append('/home/pratheek/workspace/botathon/movietimeBot')


# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movietimeBot.settings')

# import django
# django.setup()

from models import UserSteps, PlotLine, MovieProperties

from spacy.en import English
nlp = English()

from nltk.corpus import stopwords
from nltk import word_tokenize
stop = stopwords.words('english')

import random

def actor_suggestion():
	m = MovieProperties.objects.filter(color__exact='Color').order_by('-gross')[:30]
	res = []
	for item in m:
		if random.random() > 0.8:
			res.append(item.actor_1_name.encode('ascii','ignore'))
	return res[:5]

def movie_suggestion_by_actor(actor_name):
	m = MovieProperties.objects.filter(actor_1_name__iexact=actor_name)
	res = []
	for item in m:
		res.append(item.movie_title.encode('ascii','ignore'))
	return res[:5]

def movie_suggestion_by_director(director_name):
	m = MovieProperties.objects.filter(director_name__iexact=director_name)
	res = []
	for item in m:
		res.append(item.movie_title.encode('ascii','ignore'))
	return res


def movie_suggestion_by_genre(genre_name):
	g = Genre.objects.get(genrename=genre_name)
	m = MovieProperties.objects.filter(genre=g).order_by('-gross')[:10]
	res = []
	for item in m:
		res.append(item.movie_title.encode('ascii','ignore'))
	return res	

def get_response(user_id, step):
	step = UserSteps.objects.get(userId=user_id, UserStep=step)
	context = step.context


def get_subtree_for_objects(tokens, subjects):
	subject_map = {}
	subjects_hierarchy = []
	for n in tokens:
		if n.dep_ in ['pobj','dobj']:
			subjects_hierarchy.insert(n.i, n)
	for subject in subjects:
		verb = subject.head
		nodes = []
		for n in verb.subtree:
			nodes.append(n)
		subject_map[subject] = nodes
	# print subjects_hierarchy
	iterator = iter(subjects_hierarchy)
	for subject in iterator:
		try:
			next_subject = next(iterator)
			for n in subject_map[next_subject]:
				subject_map[subject].remove(n)
		except:
			break
	return subject_map

def remove_prefix_stopword(text):
	words = word_tokenize(text)
	if words == []:
		return None
	if words[0] in  stop:
		return " ".join(words[1:]).strip()
	else:
		return None


def get_movie_plot(response):
	tokens = nlp(unicode(response))

	root_verb = True
	# for tok in tokens:
	# 	print tok, tok.dep_, tok.pos_
	# 	if tok.dep_ == 'ROOT':
	# 		if tok.pos_ == 'VERB':
	# 			root_verb = True
	# print root_verb,"root_verb"
	# if root_verb:
	if 'something' in response:
		subtree = get_subtree_on_other_side_of_keyword('something', tokens)
		res = PlotLine.objects.filter(plotname__icontains=subtree)
		new_subtree = remove_prefix_stopword(subtree)
		print subtree, new_subtree
		res1 = PlotLine.objects.filter(plotname__icontains=new_subtree)
		print res,res1
		if len(res) == 0 and len(res1) == 0:
			return None
		elif len(res) != 0:
			return res[0].plotname
		elif len(res1) != 0:
			return res1[0].plotname
		else:
			return None
	elif 'movie' in response:
		subtree = get_subtree_on_other_side_of_keyword('something', tokens)
		res = PlotLine.objects.filter(plotname__icontains=subtree)
		new_subtree = remove_prefix_stopword(subtree)
		print subtree, new_subtree
		res1 = PlotLine.objects.filter(plotname__icontains=new_subtree)
		print res,res1
		if len(res) == 0 and len(res1) == 0:
			return None
		elif len(res) != 0:
			return res[0].plotname
		elif len(res1) != 0:
			return res1[0].plotname
		else:
			return None
	else:
		object_tok = None
		for tok in tokens:
			if tok.dep_ in ['dobj', 'pobj']:
				object_tok = tok
		if object_tok != None:
			objects = get_subtree_for_objects(tokens, [object_tok])
			if object_tok.text in objects:
				subtree = " ".join(res[object_tok.text]).strip()
			else:
				return None
			res = PlotLine.objects.filter(plotname__icontains=subtree)
			new_subtree = remove_prefix_stopword(subtree)
			res1 = PlotLine.objects.filter(plotname__icontains=new_subtree)
			if len(res) == 0 and len(res1) == 0:
				return None
			elif len(res) != 0:
				return res[0].plotname
			elif len(res1) != 0:
				return res1[0].plotname
			else:
				return None


def get_subtree_on_other_side_of_keyword(keyword, tokens, return_string=True):
	root = None
	left = ''
	right = ''
	subtree = ''
	subtree_tokens = None
	for t in tokens:
		if t.dep_ == 'ROOT':
			root = t
			break

	for t in root.subtree:
		if t.i < root.i:
			left += t.string
		elif t.i > root.i:
			right += t.string
	if keyword in left.lower():
		subtree = right
		subtree_tokens = tokens[root.i + 1:]
	elif keyword in right.lower():
		subtree = left
		subtree_tokens = tokens[:root.i]

	if return_string:
		return subtree
	else:
		return subtree_tokens

# a movie which involves stealing a car

# if __name__ == '__main__':
# print get_movie_plot("movie which involves stealing a car")