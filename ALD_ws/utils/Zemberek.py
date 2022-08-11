import jpype

class Zemberek(object):
    """
    This is the class for handling zemberek operations.
    """

    def __init__(self, jar_path, source_dir=None, target_dir=None, call_center=True):
        """
        :param jar_path: jar file's path.
        """

        self.zemb_dict = {}
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.call_center = call_center
        self.__out_file = "callcenter.txt"

        self.surface = False
        self.suffix = True

        jpype.startJVM(jpype.getDefaultJVMPath(),
                       "-Djava.class.path=" + jar_path,
                       "-ea")

        self.__bool_dict = {True: jpype.java.lang.Boolean(True), False: jpype.java.lang.Boolean(False)}

        morphology = jpype.JClass(
            "zemberek.morphology.analysis.tr.TurkishMorphology").createWithDefaults()  # initialize zemberek dicts
        disambiguator = jpype.JClass(
            "zemberek.morphology.ambiguity.Z3MarkovModelDisambiguator")()  # to choose best suffixes for given word
        self.__text2zemb = jpype.JClass("zemberek.morphology.hiddenslate.JsonHandler")
        self.__cc_cleaner = jpype.JClass("zemberek.morphology.hiddenslate.CallCenterCleaner")
        self.__text_cleaner = jpype.JClass("zemberek.morphology.hiddenslate.SeperateDirectory")

        self.sentence_analyze = jpype.JClass("zemberek.morphology.analysis.tr.TurkishSentenceAnalyzer")(morphology,
                                                                                                        disambiguator)

    def seperate_sentence(self, sentence):
        result = self.sentence_analyze.analyze(sentence)
        self.sentence_analyze.disambiguate(result)
        output = []
        for entry in result.iterator():
            current_part = entry.parses.get(0)
            oneword = []
            lemma = current_part.getLemma()
            oneword.append(lemma.lower() if lemma != "UNK" else current_part.getRoot().lower())
            for item in current_part.suffixDataList:
                if item.surface.strip():
                    current = []
                    if self.surface:
                        current.append("_")
                        current.append(item.surface)
                    if self.suffix:
                        current.append("_")
                        current.append(item.suffix.__str__())
                    oneword.append("".join(current).lower())
            output.append(" ".join(oneword))
        return " ".join(output)

    def fit(self):
        pass

    def text2zemb(self, source, target):
        self.__text2zemb.main(source, target, self.__bool_dict[self.surface], self.__bool_dict[self.suffix])

    def transform(self, *args, **kwargs):
        if not isinstance(self.call_center, bool):
            raise Exception("call_center must be a boolean!")
        if self.call_center:
            self.__cc_cleaner.main(self.source_dir, self.target_dir, self.__bool_dict[self.surface],
                                   self.__bool_dict[self.suffix])
            return self.target_dir + self.__out_file
        else:
            self.__text_cleaner.main(self.source_dir, self.target_dir, self.__bool_dict[self.surface],
                                     self.__bool_dict[self.suffix])

    def _zemb2word(self, lis, original):
        if lis:
            return self.zemb_dict.get(" ".join(lis), self._zemb2word(lis[:-1], original))
        else:
            return " ".join(original).strip()

    def merge_sentence(self, sentence):
        word_list = []
        current = []
        for token in sentence.strip().split():
            if token.startswith("_"):
                current.append(token)
            else:
                word_list.append(current)
                current = [token]
        if word_list[-1] != current:
            word_list.append(current)

        output = []
        for word in word_list:
            output.append(self._zemb2word(word, word))

        return " ".join(output).strip()

    def create_dict(self, map_file):
        for line in open(map_file):
            key, value = line.strip().split("\t")
            self.zemb_dict[key] = value
        print("Zemberek mapping object has been created!")
















# import jpype
#
#
# class Zemberek(object):
#     """
#     This is the class for handling zemberek operations.
#     """
#
#     def __init__(self, jar_path):
#         """
#         :param jar_path: jar file's path.
#         """
#         jpype.startJVM(jpype.getDefaultJVMPath(),
#                        "-Djava.class.path="+jar_path,
#                        "-ea")
#         morphology = jpype.JClass("zemberek.morphology.analysis.tr.TurkishMorphology").createWithDefaults()  #initialize zemberek dicts
#         disambiguator = jpype.JClass("zemberek.morphology.ambiguity.Z3MarkovModelDisambiguator")()  #to choose best suffixes for given word
#         self.sentence_analyze = jpype.JClass("zemberek.morphology.analysis.tr.TurkishSentenceAnalyzer")(morphology, disambiguator)
#         self.fil = jpype.JClass("zemberek.morphology.hiddenslate.SeperateFile")
#
#     def seperate_sentence(self,sentence):
#         result = self.sentence_analyze.analyze(sentence)
#         self.sentence_analyze.disambiguate(result)
#         output = ""
#         for entry in result.iterator():
#             current_part = entry.parses.get(0)
#             if current_part.getLemma() == "UNK":
#                 output += current_part.getRoot()
#             else:
#                 output += current_part.getLemma()
#             for i in range(len(current_part.suffixSurfaceList())):
#                 suffix = current_part.suffixSurfaceList()[i]
#                 if len(suffix) > 0:
#                     output += " _" + suffix
#             output += " "
#         return output.replace('İ','i').lower()
#
#     def seperate_file(self, src, tgt):
#         """
#         applying zemberek operation to a file
#         :param src: source file
#         :param tgt: target file
#         :return: Nothing
#         """
#         self.fil.main([src, tgt])
#
#     def close(self):
#         jpype.shutdownJVM()
