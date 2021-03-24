# txtProcessor is a mini helper library to support pptWizard's processes
# It contains functions necessary for text analysis and adaptation

# Filter() function filters out all the unwanted characters from a text or a word
def Filter(litter, string):
    # See if the string includes any spaces:
    if " " in string:
        # Split the string into separate words
        text = string.split()
        words = []
        for word in text:
            if word in litter:
                continue
            words.append(word)
        new_string = " ".join(words)
    # If the string doesn't include any spaces
    else:
        chars = []
        # Remove all the litter symbols
        for char in string:
            if char in litter:
                continue
            chars.append(char)
        new_string = "".join(chars)
    return new_string
# filterChars() is an additional function to the Filter(), that allows to filter every single word from a text in a simplified manner
def filterChars(litter, string):
    # Split the string into words
    words = string.split()
    for word in words:
        # Replace every word with a filtered version
        words[words.index(word)] = Filter(litter, word)
    # Join them back into a string
    new_string = " ".join(words)
    return new_string
# findKeywords finds the most frequent words and word combinations in a text
def findKeywords(text):
    # Filter the text from the conjunctions and the punctuation marks
    text = noJoints(text)
    # Split the text into separate words
    words = text.split()
    # If the paragraph was a list item that is too short,
    # Then the whole thing itself has to be the keywords
    if len(words) < 8:
        return text
    # Collect all the word trios
    trios = []
    i = 0
    while i < len(words)-2:
        trios.append(words[i]+" "+words[i+1]+" "+words[i+2])
        i += 1
    # Count how many times each trio repeats itself
    amounts = []
    for trio in trios:
        amounts.append(trios.count(trio))
    freq3 = max(amounts)
    trio = trios[amounts.index(freq3)]

    # Collect all the word pairs
    pairs = []
    i = 0
    while i < len(words)-1:
        pairs.append(words[i]+" "+words[i+1])
        i += 1
    # Count how many times each pair repeats itself
    amounts = []
    for pair in pairs:
        amounts.append(pairs.count(pair))
    freq2 = max(amounts)
    pair = pairs[amounts.index(freq2)]

    # See which single word appears the most often
    amounts = []
    for word in words:
        amounts.append(words.count(word))
    freq1 = max(amounts)
    word = words[amounts.index(freq1)]

    # Remove the combinations of words that only appear once
    combs = [word, pair, trio]
    freqs = [freq1, freq2, freq3]
    thrash = []
    i = 0
    while i < len(combs):
        if freqs[i] == 1:
            thrash.append(combs[i])
            combs.remove(combs[i])
            continue
        i += 1
    # Handle the case when there are no repeating words
    if len(combs) == 0:
        keywords = thrash[len(thrash)-1]
    # Choose the keyword based on the highest rank of combination
    else:
        keywords = combs[len(combs)-1]
    return keywords
# formatTitle() is meant to make sure that the title won't contatin characters that are not allowed for a directory name
def formatTitle(title):
    forbidden = ['\\','/',':','*','?','"','<','>','|']
    new_title = filterChars(forbidden, title)
    return new_title
# A function for extracting html tables in a normal structure
def formatTable(table):
    t = []
    rows = table.find_all("tr")
    for row in rows:
        t.append(row.text+" ")
    t = "\n".join(t)
    return t
# noJoints removes all the conjunctions and punctuation marks from a text in order to simplify text analysis
def noJoints(text):
    # Define all the conjunctions and punctuation marks
    punct = [".",",",":","-",";",'"',"&",
            '\\','/',':','*','?','"','<','>','|']
    conj = [
            "-", "a", "the",
            "and", "of", "if",
            "into", "in", "on",
            "upon", "onto", "so",
            "that", "this", "it",
            "thus", "to", "what",
            "such", "those", "these",
            "is", "an", "for",
            "there", "are", '–',
            "also", "under", "will",
            "be", "by", "with",
            "as", "would", "have",
            "has", "will", "was",
            "were", "here", "could",
            "or",
            # Conjunctions in Russian
            "и","в","на","над","из",
            "для","с","под",
            ]
    new_text = Filter(conj, filterChars(punct, text))
    return new_text
# identifyTopic() will see which of the words from the title appear most often in the paragraphs of the article
def identifyTopic(article):
    # Remove all the forbidden characters from the title and split it into separate words
    title = formatTitle(noJoints(article[0]).lower()).split()
    text = article[2]
    # See how often each word appears in the text
    freqs = []
    for word in title:
        count = 0
        for paragraph in text:
            count += noJoints(paragraph.lower()).count(word)
        freqs.append(count)
    # Identify two keywords by the highest frequences
    keyword1 = title[freqs.index(max(freqs))]
    freqs.remove(max(freqs))
    keyword2 = title[freqs.index(max(freqs))]
    topic = keyword1 + " " + keyword2
    return topic
# This function is to make sure that no paragraphs exceed the character limit on the future slide
def Limit(structure):
    lim = 550
    # Check if any of the paragraphs exceed the characters limit
    for p in structure[2]:
        # Split the paragraph into halves and find the nearest dot
        if len(p) > lim:
            # Find the middle
            mid = int(len(p)/2)
            # Start from the middle and move backwards to find the nearest dot
            pos = mid
            # Until you meet he point
            while p[pos] != ".":
                pos -= 1
            # Then divide the paragraph in two parts at the dot
            part1 = p[:pos+1]
            part2 = p[pos+1:]
            # If the length of any of the parts is less then 10 words
            if len(part1.split()) < 10 or len(part2.split()) < 10:
                # Just go on with checking the next paragraph
                continue
            # Find the id of the current paragraph in the paragraphs list
            i = structure[2].index(p)
            # First, replace the full paragraph with its first part
            structure[2][i] = part1
            # Next insert the second part right after the first one
            structure[2].insert(i+1, part2)
            # Insert an empty headline for the second part of the paragraph
            structure[1].insert(i+1, " ")
    return structure
# stickAttachments allocates lists and tables that were following the paragraph
def stickAttachments(attachment, headlines, paragraphs):
    if attachment != None:
        # See if that's a table
        if attachment.name == "table":
            headlines.append("Table")
            paragraphs.append(formatTable(attachment))
        # See if that's a list
        else:
            for item in attachment.find_all("li"):
                # Check the length of the list item
                length = len(item.text)
                # See if its less than 20 words
                if length < 30:
                    # If so, attach it to the previous paragraph seamlessly
                    lastPar = paragraphs[len(paragraphs)-1]
                    lastPar = lastPar + item.text
                # If its >= 20 words, attach it as a separate paragraph
                else:
                    headlines.append(" ")
                    paragraphs.append(item.text)
