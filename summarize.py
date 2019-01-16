import numpy as np

text = "Bigbang Seungri has been touring since August 2018 and visited countries all over Asia for his debut solo tour 'The Great Seungri'. Last night's concert in Hong Kong left many fans shocked outraged and ready to fight. Seungri admitted that while he was rehearsing Yang Hyun Suk called him saying that since he's 'The Great Seungri' he doesn't need any back up dancers and told him to perform alone. As it later turned out all of Seungri's stylists have been sent by YG to work with BLACKPINK  while he was left with no stylist, no band and other 2 dancers as a senior artist. Meanwhile Big Bang is known to be the biggest money maker inYG and the group who made YG a part of the Big3.Currently fans express their disappointment on twitter and Yang Hyun Suk instagram trending #SeungriDeservesBetter"
title = "BIGBANG Seungri still mistreated by YG, left without back up dancers and stylists to perform on his own"

def preprocess(text):
    sentence = text.split(".")
    sentences = text.lower().split(".")
    token_sentences = []
    for i in sentences:
        token = i.split(" ")
        for j in range(len(token)):
            token[j] = token[j].replace(",","")
            token[j] = token[j].replace("?","")
            token[j] = token[j].replace("'"," ")
            token[j] = token[j].replace("!","")
            token[j] = token[j].replace("(","")
            token[j] = token[j].replace(")","")
            token[j] = token[j].replace("#","")
        token_sentences.append(token)
    return token_sentences, sentence

def F1(token_sentences):
    count = {}
    score = []
    for i in token_sentences:
        for j in i:
            if j in count:
                count[j] += 1
            else:
                count[j] = 1
    for i in token_sentences:
        each_sentences = {}
        for j in i:
            if j in each_sentences:
                each_sentences[j] += 1
            else:
                each_sentences[j] = 0
        score_per_sentences = 0
        for j in each_sentences:
            score_per_sentences += each_sentences[j]/count[j]
        score.append(score_per_sentences)
    return score

def F2(token_sentences):
    len_s = []
    for i in token_sentences:
        len_s.append(len(i))
    max_len = max(len_s)
    return list(map(lambda x: x/max_len, len_s))

def F3(token_sentences):
    position = []
    for i in range(len(token_sentences)):
        position.append((len(token_sentences)-i)/len(token_sentences))
    return position

def F4(title, token_sentences):
    title_token = preprocess(title)
    score = []
    for i in token_sentences:
        same = 0
        for title_word in title_token[0]:
            for content_word in i:
                if title_word == content_word:
                    same += 1
        score.append(same/len(title_token))
    return score

def F6(f1, f2, f3, f4):
    score = []
    for i in range(len(f1)):
        score.append(f1[i]+f2[i]+f3[i]+f4[i])
    max_score = max(score)
    return list(map(lambda x: x/max_score, score))

def summarize_content(title, text):
    x, y = preprocess(text)
    feature_1 = F1(x)
    feature_2 = F2(x)
    feature_3 = F3(x)
    feature_4 = F4(title, x)
    feature_6 = F6(feature_1, feature_2, feature_3, feature_4)
    all_feature = []

    for i in range(len(feature_1)):
        all_feature.append(feature_1[i] + feature_2[i] + feature_3[i] + feature_4[i] + feature_6[i])
    max_score = max(all_feature)
    all_feature = list(map(lambda x: x/max_score, all_feature))
    all_feature = np.array(all_feature)
    all_feature = all_feature.argsort()[::-1][:len(all_feature)]
    n = (int(len(all_feature)/3))

    summ = []
    for i in all_feature[:n]:
        summ.append(y[i])
    return '. '.join(summ)

a = summarize_content(title, text)
print(a)
