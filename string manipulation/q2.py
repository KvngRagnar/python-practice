def passing_scores(scores):
    passed = []
    for index in range(len(scores)):
        if scores[index] ==[]:
            passed.append(scores[index])
    return passed
print(passing_scores([49, 50, 80, 65]))