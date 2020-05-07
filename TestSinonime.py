import nltk
import rowordnet

wn = rowordnet.RoWordNet()


def word_similarity(word1, word2):
    synsets1 = wn.synsets(literal=word1)
    if not synsets1:
        return 0
    synsets2 = wn.synsets(literal=word2)
    if not synsets2:
        return 0
    path_length = len(wn.shortest_path(synsets1[0], synsets2[1]))
    return 1 / path_length ** 2


synsets = wn.synsets(literal="cauza")
print(len(synsets))
for syn in synsets:
    wn.print_synset(syn)

# synset_ids = wn.synsets(literal=word1)
# syn_set = set()
# for synset_id in synset_ids:
#     synset_object = wn.synset(synset_id)
#     syn_list = [lit for lit in synset_object.literals if "-" not in lit]
#     syn_set.update(syn_list)
# print(syn_set)
