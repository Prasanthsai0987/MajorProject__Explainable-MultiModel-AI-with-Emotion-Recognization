def compare_phonemes(expected, spoken):

    correct = 0

    for e, s in zip(expected, spoken):
        if e == s:
            correct += 1

    score = correct / len(expected)

    return score


# zip is a built-in Python function that takes two or more iterables, it pairs up the expected and spoken phonemes for comparison.