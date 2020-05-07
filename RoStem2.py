import string
from chatFun import greeting, response, read_json, stemSentence

# read file, json is imported as a dict {intent:response}
my_dict = read_json("depresie.json")

# break dict in sentences and responses
sent_tokens = [k for (k, v) in my_dict.items()]
responses = [v for (k, v) in my_dict.items()]

# Remove punctuation marks from sentences
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
sent_tokens = [sent.translate(remove_punct_dict) for sent in sent_tokens]

print(stemSentence(sent_tokens[1]))

flag = True
print("ROBO: Ma numesc ROBO. Voi raspunde intrebarilor despre depresie. Daca vrei sa iesi scrie pa")
while flag:
    user_response = input()
    user_response = user_response.lower()
    if user_response != 'pa':
        if greeting(user_response) is not None:
            print("ROBO: " + greeting(user_response))
        else:
            print("ROBO: ", end="")
            print(response(user_response, sent_tokens, responses))
            sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Sanatate!")
