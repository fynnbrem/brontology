import en_core_web_trf

nlp = en_core_web_trf.load()

tok = nlp("I love Python.")[1]


nlp.vocab.lookup_lemma()