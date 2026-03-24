from nltk.tokenize import word_tokenize


def lexical_diversity_measurements(book):

        tokens = word_tokenize(book)
        words = []
        unique_words = []
        word_once_occurencing = []
        
        for word in tokens :

            if word not in ["",".","!",",","?",";",":","/"] :
                words.append(word)

                if word not in unique_words :
                    unique_words.append(word)

                if tokens.count(word) == 1:
                    word_once_occurencing.append(word)            

        return {
            "tok":len(words),
            "typ":len(unique_words),
            "hap":len(word_once_occurencing),
            "ttr":len(unique_words)/len(words),
            "mwl":sum(len(word) for word in words) / len(words),
            "mwf":len(words)/len(unique_words)
        }
