#LR2- Фильтрация массива с учетом регистра строки


words=[]
def find_in_different_registers(words: list[str]):
    unique_words = set()
    result = []

    for word in words:
        normalized_word = word.lower()

        if normalized_word not in unique_words:
            unique_words.add(normalized_word)
            result.append(word)
        else:
            result = [w for w in result if w.lower() != normalized_word]

    return result


print(find_in_different_registers(words))

