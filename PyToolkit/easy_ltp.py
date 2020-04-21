# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     easy_ltp
   Description :
   Author :       Liangs
   date：          2019/5/7
-------------------------------------------------
   Change Activity:
                   2019/5/7:
-------------------------------------------------
"""
import os
import pyltp
import re


class EasyLTP(object):
    def __init__(self, ltp_path, dependency=False):
        self.dependency = dependency
        cws_model_path = os.path.join(ltp_path, 'cws.model')
        pos_model_path = os.path.join(ltp_path, 'pos.model')
        ner_model_path = os.path.join(ltp_path, 'ner.model')
        dp_model_path = os.path.join(ltp_path, 'parser.model')
        self.seg = pyltp.Segmentor()
        self.pos = pyltp.Postagger()
        self.ner = pyltp.NamedEntityRecognizer()
        # self.srl = pyltp.SementicRoleLabeller()
        self.seg.load(cws_model_path)
        self.pos.load(pos_model_path)
        self.ner.load(ner_model_path)
        # self.srl.load(srl_model_path)
        if dependency:
            self.dp = pyltp.Parser()
            self.dp.load(dp_model_path)

    def seg_sent(self, sent):
        words = self.seg.segment(sent)
        return [str(w) for w in words]

    def pos_sent(self, sent):
        words = self.seg.segment(sent)
        poss = self.pos.postag(words)
        return [str(p) for p in poss]

    def pos_words(self, words):
        poss = self.pos.postag(words)
        return [str(p) for p in poss]

    def ner_sent(self, sent):
        # Nh:人名
        # Ni:机构名
        # Ns:地名
        words = self.seg.segment(sent)
        poss = self.pos.postag(words)
        ners = self.ner.recognize(words, poss)
        ner_ch = []
        for n in ners:
            if str(n).endswith('Nh'):
                ner_ch.append(str(n).replace('Nh', 'person'))
            elif str(n).endswith('Ni'):
                ner_ch.append(str(n).replace('Ni', 'organization'))
            elif str(n).endswith('Ns'):
                ner_ch.append(str(n).replace('Ns', 'location'))
            else:
                ner_ch.append(str(n))
        return ner_ch

    def ner_words(self, words):
        poss = self.pos.postag(words)
        ners = self.ner.recognize(words, poss)
        ner_ch = []
        for n in ners:
            if str(n).endswith('Nh'):
                ner_ch.append(str(n).replace('Nh', 'person'))
            elif str(n).endswith('Ni'):
                ner_ch.append(str(n).replace('Ni', 'organization'))
            elif str(n).endswith('Ns'):
                ner_ch.append(str(n).replace('Ns', 'location'))
            else:
                ner_ch.append(str(n))
        return ner_ch

    def seg_with_ner_sent(self, sentence):
        words = self.seg_sent(sentence)
        ners = self.ner_words(words)
        new_words = []
        cat_word = ''
        for word, ner in zip(words, ners):
            if ner[0] in ['O', 'S']:
                new_words.append(word)
            elif ner[0] in ['B', 'I']:
                cat_word += word
            elif ner[0] == 'E':
                cat_word += word
                new_words.append(cat_word)
                cat_word = ''
            else:
                raise ValueError(f'bad ner value:{ner}')
        return new_words

    def extract_named_entity_words(self, sent):
        words = self.seg.segment(sent)
        poss = self.pos.postag(words)
        ners = self.ner.recognize(words, poss)
        ner_ch = []
        for n in ners:
            if str(n).endswith('Nh'):
                ner_ch.append(str(n).replace('Nh', 'person'))
            elif str(n).endswith('Ni'):
                ner_ch.append(str(n).replace('Ni', 'organization'))
            elif str(n).endswith('Ns'):
                ner_ch.append(str(n).replace('Ns', 'location'))
            else:
                ner_ch.append(str(n))
        named_entity = []
        cat_words = ''
        for word, ner in zip(words, ner_ch):
            if ner[0] == 'O':
                continue
            if ner[0] in ['B', 'I']:
                cat_words += word
            elif ner[0] == 'E':
                cat_words += word
                named_entity.append((cat_words, ner.split('-')[-1]))
                cat_words = ''
            elif ner[0] == 'S':
                named_entity.append((word, ner.split('-')[-1]))
        return list(set(named_entity))

    def dependency_sent(self, sent):
        words = list(self.seg.segment(sent))
        words_root = ['Root'] + words
        poss = self.pos.postag(words)
        arcs = self.dp.parse(words, poss)
        result = []
        for arc, (child_index, child_word) in zip(arcs, enumerate(words)):
            result.append(((arc.head, words_root[arc.head]), arc.relation, (child_index + 1, child_word)))
        return result

    def judge_sent_by_dependency(self, sentence):
        """
            判读root指向的词是否发出了SBV弧，一种非常简单的判断句子完整性的方式
        """
        dependency = self.dependency_sent(sentence)
        core_word_idx = -1
        for dep in dependency:
            if dep[0][0] == 0 and dep[1] == 'HED':
                core_word_idx = dep[2][0]
        # print(core_word_idx)
        if core_word_idx == -1:
            return False
        for dep in dependency:
            if dep[1] == 'SBV' and dep[0][0] == core_word_idx:
                return True
        return False

    def release(self):
        self.seg.release()
        self.pos.release()
        self.ner.release()


if __name__ == '__main__':
    pass
