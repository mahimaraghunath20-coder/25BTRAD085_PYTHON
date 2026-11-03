words = input("Enter a sentence: ")

frequency = {}

for word in words.split():
    if word in frequency:
        frequency[word] += 1
    else:
        frequency[word] = 1

print("\nWord Frequencies:")

for word, count in frequency.items():
    print(word, ":", count)