# -*- coding: utf-8 -*-

from verbecc import inflector

class InflectorRo(inflector.Inflector):
    def __init__(self):
        self.lang = 'ro'
        super(InflectorRo, self).__init__()

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        if mood_name == 'imperativ' and tense_name == 'negativ':
            return 'nu ' + s
        return s

    """TODO: There are two types of reflexive verbs in Romanian: 
    preceded by the reflexive pronouns “se” (in the accusative) and “și” (in the dative).
    """

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'eu'
            if is_reflexive:
                ret += ' mă'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'el'
            if gender == 'f':
                ret = 'ea'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'noi'
            if is_reflexive:
                ret += ' ne'
        elif person == '2p':
            ret = 'voi'
            if is_reflexive:
                ret += ' vă'
        elif person == '3p':
            ret = 'ei'
            if gender == 'f':
                ret = 'ele'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return ['participiu', 
                'afirmativ', 
                'imperativ', 'negativ', 
                'gerunziu']

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        if tense_name in ('viitor-1', 'viitor-2'):
            return 'voi'
        return 'avea'

    def _get_subjunctive_mood_name(self):
        return 'conjunctiv'

    def _get_participle_mood_name(self):
        return 'participiu'

    def _get_participle_tense_name(self):
        return 'participiu'

    def _get_compound_conjugations_hv_map(self):
        return {
            'indicativ': {
                'perfect-compus': 'prezent',
                'viitor-1': 'prezent',
                'viitor-2': 'prezent'
            }
        }

    def _auxilary_verb_uses_alternate_conjugation(self, tense_name):
        return tense_name in ('viitor-1', 'viitor-2')

    def _conjugate_compound_primary_verb(self, co, mood_name, tense_name, persons, aux_verb, aux_conj):
        if mood_name == 'indicativ' and tense_name == 'viitor-1':
            return [hv + ' ' + co.verb.infinitive for hv in aux_conj]
        conj = super(InflectorRo, self)._conjugate_compound_primary_verb(
            co, mood_name, tense_name, persons, aux_verb, aux_conj)
        if mood_name == 'indicativ' and tense_name == 'viitor-2':
            conj_mod = []
            for pronoun, hv, participle in [c.split(' ') for c in conj]:
                conj_mod += [' '.join([pronoun, hv, 'fi', participle])]
            conj = conj_mod
        return conj
