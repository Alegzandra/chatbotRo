import string

from chatFun import greeting, response, read_json, stemSentence, syn_response, to_sentence_list, remove_punctuation, \
    remove_stop_words_from_list

sent_tokens = to_sentence_list("faq.txt")
responses = sent_tokens
sent_tokens = remove_punctuation(sent_tokens)
sent_tokens = remove_stop_words_from_list(sent_tokens)

flag = True
print("ROBO: Ma numesc ROBO. Voi raspunde intrebarilor tale. Daca vrei sa iesi scrie pa")
while flag:
    user_response = input()
    user_response = user_response.lower()
    if user_response != 'pa':
        if greeting(user_response) is not None:
            print("ROBO: " + greeting(user_response))
        else:
            print("ROBO: ", end="")
            print(syn_response(user_response, sent_tokens,responses))
    else:
        flag = False
        print("ROBO: Sanatate!")
