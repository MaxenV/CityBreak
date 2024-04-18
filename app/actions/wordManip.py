import morfeusz2


class WordManip:
    def __init__(self):
        self.morf = morfeusz2.Morfeusz()

    def to_nominative(self, word):
        analysis = self.morf.analyse(word[0].upper() + word[1:].lower())
        for i in analysis:
            if "nazwa_geograficzna" in i[-1][-2]:
                return i[-1][1].split(":")[0]
        return word
