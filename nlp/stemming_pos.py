#!pip install spacy
#!python -m spacy download en
import spacy
nlp=spacy.load('en')
sentence="Trump imposed tariffs on China against the EU leaders' advice."

for token in nlp(sentence):
   print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop, token.ent_type_,)

#lemma kertoo sanan perusmuodon, pos kertoo sanasta mikä osa lausetta se on, tag saman kuin pos mutta tarkemmin, dep kertoo sanojen
#riippuvuuden toisistaan lauseessa, kertoo sanan muodon isot kirjaimet numeraalit jne, alpha kertoo onko sana alfanumeerinen ja stop
#kertoo onko sana kielen käytetyimpiä