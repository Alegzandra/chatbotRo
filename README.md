# Chatbot in Romanian using synonyms #

## How synonyms are used ##

Synset instances are the groupings of synonymous words that express the same concept. 

A synset has the following data, accessed as properties (others are present, but the following are most important):

* id : the id(string) of this synset
* literals : a list of words(strings) representing a unique concept. These words are synonyms.
* definition : a longer description(string) of this synset
* pos : the part of speech of this synset (enum: Synset.Pos.NOUN, VERB, ADVERB, ADJECTIVE)
* sentiwn : a three-valued list indicating the SentiWN PNO (Positive, Negative, Objective) of this synset.
* Relations are edges between synsets

Eg.

    synsets = wn.synsets(literal="cauza")
    print(len(synsets))
    for syn in synsets:
        wn.print_synset(syn)

    3
    Synset: 
	  id=ENG30-01016316-v
	  pos=VERB
	  nonlexicalized=None
	  stamp=Verginica
	  domain=factotum
	  definition=A vorbi în fața unei instanțe judecătorești (ca avocat), apărând cauza uneia dintre părți.
	  sumo=Stating 
	  sumoType=HYPERNYM
	  sentiwn=[0.0, 0.0, 1.0]
	  Literals:
		  apăra - 5.1
		  pleda - 1
		  susține_cauza_cuiva - 1
		  susține - 
		  cauza - 
		  cuiva - 
	  Outbound relations: 
		  ENG30-01016002-v - hypernym
		  ENG30-08441203-n - domain_TOPIC
		  ENG30-09775663-n - near_eng_derivat
		  ENG30-06559365-n - near_eng_derivat
		  ENG30-01016626-v - hyponym
	  Inbound relations: 
		  ENG30-08441203-n - domain_member_TOPIC
		  ENG30-07209089-n - near_eng_derivat
		  ENG30-06562802-n - near_eng_derivat
		  ENG30-01016316-v - hyponym
		  
		  Synset: 
	  id=ENG30-01646866-v
	  pos=VERB
	  nonlexicalized=None
	  stamp=Catalin Mihaila
	  domain=factotum
	  definition=A avea drept urmare
	  sumo=Process 
	  sumoType=HYPERNYM
	  sentiwn=[0.0, 0.0, 1.0]
	  Literals:
		  aduce - 5.x
		  cauza - 1.2.x
		  pricinui - 1.2.x
		  produce - 4.2
		  provoca - 2.1
	  Outbound relations: 
		  ENG30-01645601-v - hypernym
		  ENG30-05827253-n - near_eng_derivat
		  ENG30-09184975-n - near_eng_derivat
		  ENG30-01629958-v - verb_group
		  ENG30-01647131-v - hyponym
	  Inbound relations: 
		  ENG30-01646866-v - hyponym
		  
## How similarity between two words is computed

* if stem(word1) == stem(word2) return 1
* find synset for each word
* take first syn for each synset
* compute shortest path between the two syns (see outgoing, ingoing relations)
* return 1/path**2

## How chatbot currently works:
* list of frequently asked questions -> list of sentences that we try to match
* on the list -> remove punctuation, stop words in Romanian (stopwords-ro.txt)

eg. 

['am gresit datele de facturare.', 'se poate refactura comanda.', 'am primit un card cadou si am incercat sa il folosesc la o comanda, dar nu se aplica.', 'ce trebuie sa fac.', 'am pierdut cardul cadou.', 'cum il recuperez.', 'am achizitionat garantia plus, cum pot trimite produsul defect in service.', 'am primit un produs defect de nou (doa), ce trebuie sa fac.', 'care este avantajul unei comenzi online.',

['gresit datele facturare', 'refactura comanda', 'primit card cadou incercat folosesc comanda aplica', 'trebuie fac', 'pierdut cardul cadou', 'recuperez', 'achizitionat garantia trimite produsul defect service', 'primit produs defect doa trebuie fac', 'avantajul comenzi online'

* take user response from input
* for each word in the user response find similarity with each word in a candidate sentence. 
add similarity, divide by number of words -> candidate sentence score
* do above step for each candidate sentence, return sentence with highest score

## Problems/TODOs
* wn.synsets(literal="masina") returns no synsets :(
* need to calibrate on domain text
* need to apply inverse document frequency -> assign a lower score to common words

### Files used ###
* stopwords-ro.txt
* faq.txt
* chatFun.py
* RoStem3.py

### See also
https://wordnet.princeton.edu/

https://github.com/dumitrescustefan/RoWordNet


```puml
User -> RoStem : message
activate RoStem #Coral
RoStem -> chatFun : synResponse(message)
activate chatFun #CadetBlue
loop for sen in sentence list
    chatFun -> chatFun : sentence_similarity(message, sen)
    activate chatFun #DarkOliveGreen
    loop for w1,w2 in message,sen
        chatFun -> chatFun : word_similarity (w1,w2)
        activate chatFun #DarkSalmon
        deactivate chatFun
    end
    deactivate chatFun
end 
chatFun --> RoStem : response
deactivate chatFun
RoStem --> User
deactivate RoStem
```
