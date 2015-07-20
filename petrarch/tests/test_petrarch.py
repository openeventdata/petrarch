from petrarch import petrarch, PETRglobals, PETRreader, utilities


config = petrarch.utilities._get_data('data/config/', 'PETR_config.ini')
print("reading config")
petrarch.PETRreader.parse_Config(config)
print("reading dicts")
petrarch.read_dictionaries()
petrarch.start_logger()


def test_version():
    assert petrarch.get_version() == "0.4.0"


def test_read():
    assert "RUSSIA" in petrarch.PETRglobals.ActorDict

######################################
#
#       Full sentence tests
#
######################################

def test_simple():
    text = "Germany invaded France"
    parse = "(ROOT (S (NP (NNP Germany)) (VP (VBD invaded) (NP (NNP France)))))"
    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parse}},
                u'meta': {u'date': u'20010101'}}}

    return_dict = petrarch.do_coding(dict,None)
    print(return_dict)
    assert return_dict['test123']['sents']['0']['events'] == [['DEU','FRA','192']]

def test_simple2():
    text = "Germany arrested France"
    parse = "(ROOT (S (NP (NNP Germany)) (VP (VBD arrested) (NP (NNP France)))))"
    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parse}},
                u'meta': {u'date': u'20010101'}}}

    return_dict = petrarch.do_coding(dict,None)
    print(return_dict)
    assert return_dict['test123']['sents']['0']['events'] == [['DEU','FRA','173']]


def test_complex1():

    text = "A Tunisian court has jailed a Nigerian student for two years for helping young militants join an armed Islamic group in Lebanon, his lawyer said Wednesday."

    parse = """( (S (S
    (NP (DT A) (NNP Tunisian) (NN court))
    (VP (AUXZ has)
    (VP (VBN jailed)
    (NP (DT a) (JJ Nigerian) (NN student))
    (PP (IN for)
    (NP (CD two) (NNS years)))
    (PP (IN for) (S
    (VP (VBG helping) (S
    (NP (JJ young) (NNS militants))
    (VP (VB join)
    (NP (NP (DT an) (JJ armed) (JJ Islamic) (NN group))
    (PP (IN in)
    (NP (NNP Lebanon)))))))))))) (, ,)
    (NP (PRP$ his) (NN lawyer))
    (VP (VBD said)
    (NP (NNP Wednesday))) (. .)))"""


    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parse}},
                u'meta': {u'date': u'20010101'}}}

    return_dict = petrarch.do_coding(dict,None)
    assert return_dict['test123']['sents']['0']['events'] == [['TUNJUD','NGAEDU','173']]


def test_nested():

    # In PETRARCH 0.4.0 this event should only code "US claimed that ISIL."
    # Nested sentences are intentionally not coded, but this can be changed if needed.
    #       (this would be changed at the end of check_verbs where the index is reevaluated)
    
    
    text = "The US claimed that ISIL had attacked Iraq and taken the city of Mosul"

    parse = """(ROOT (S (NP (DT The) (NNP US)) (VP (VBD claimed) (SBAR (IN that) (S (NP (NNP ISIL)) (VP (VBD had) (VP (VP (VBN attacked) (NP (NNP Iraq))) (CC and) (VP (VBN taken) (NP (NP (DT the) (NN city)) (PP (IN of) (NP (NNP Mosul))))))))))))"""

    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parse}},
                u'meta': {u'date': u'20150101'}}}

    return_dict = petrarch.do_coding(dict,None)
    assert return_dict['test123']['sents']['0']['events'] == [['USA','IMGMUSISI','112']]


def test_actor_order():

    text = "US troops from Syria have just invaded Northern Iraq"

    parse = """(ROOT (S (NP (NP (NNP US) (NNS troops)) (PP (IN from) (NP (NNP Syria)))) (VP (VBP have) (ADVP (RB just)) (VP (VBN invaded) (NP (JJ Northern) (NNP Iraq))))))"""

    parsed = utilities._format_parsed_str(parse)

    dict = {u'test123': {u'sents': {u'0': {u'content': text, u'parsed': parse}},
                u'meta': {u'date': u'20150101'}}}

    return_dict = petrarch.do_coding(dict,None)
    assert return_dict['test123']['sents']['0']['events'] == [['USAMIL','IRQ','192']]


#########################################
#
#       Individual function tests
#
#########################################

def test_check_balance():
    petrarch.check_balance(['(','~'])

    try:
        petrarch.check_balance(['(','~','~'])
        assert False
    except:
        assert True

    list = [u'(', u'(S', u'(NP1', u'(NE', u'---', u'A', u'500-PAGE', u'REPORT', u'~NE', u'(VP1', u'(VBN', u'RELEASED', u'~VBN', u'(NE', u'---', u'TUESDAY', u'~NE', u'(PP', u'(IN', u'IN', u'~IN', u'(NE', u'---', u'THE', u'RWANDAN', u'CAPITAL', u'~NE', u'~PP', u'~VP1', u'~NP1', u'(VP2', u'(VP3', u'(VBD', u'ALLEGED', u'~VBD', u'(SBAR', u'(SBAR', u'(IN', u'THAT', u'~IN', u'(S', u'(NE', u'---', u'FRANCE', u'~NE', u'(VP4', u'(VBD', u'WAS', u'~VBD', u'(ADJP', u'(JJ', u'AWARE', u'~JJ', u'(PP', u'(IN', u'OF', u'~IN', u'(NE', u'---', u'PREPARATIONS', u'FOR', u'THE', u'GENOCIDE', u'~NE', u'~PP', u'~ADJP', u'~VP4', u'~S', u'~SBAR', u'(,', u',', u'~,', u'(CCP', u'AND', u'~CCP', u'(SBAR', u'(IN', u'THAT', u'~IN', u'(S', u'(NE', u'---', u'THE', u'FRENCH', u'MILITARY', u'IN', u'RWANDA', u'~NE', u'(VP5', u'(VBD', u'CONTRIBUTED', u'~VBD', u'(PP', u'(TO', u'TO', u'~TO', u'(S', u'(VP6', u'(VBG', u'PLANNING', u'~VBG', u'(NE', u'---', u'THE', u'MASSACRES', u'~NE', u'~VP6', u'~S', u'~PP', u'~VP5', u'~S', u'~SBAR', u'~SBAR', u'~VP3', u'(CCP', u'AND', u'~CCP', u'(VP7', u'(ADVP', u'(RB', u'ACTIVELY', u'~RB', u'~ADVP', u'(VBD', u'TOOK', u'~VBD', u'(NE', u'---', u'PART', u'IN', u'THE', u'KILLING', u'~NE', u'~VP7', u'~VP2', u'(.', u'.', u'~.', u'~S', u'~']


    petrarch.check_balance(list)

    try:
        petrarch.check_balance(list[1:])
        assert False
    except:
        assert True



def test_read_treebank():

    list = [u'(', u'(S', u'(NP1', u'(NE', u'---', u'A', u'500-PAGE', u'REPORT', u'~NE', u'(VP1', u'(VBN', u'RELEASED', u'~VBN', u'(NE', u'---', u'TUESDAY', u'~NE', u'(PP', u'(IN', u'IN', u'~IN', u'(NE', u'---', u'THE', u'RWANDAN', u'CAPITAL', u'~NE', u'~PP', u'~VP1', u'~NP1', u'(VP2', u'(VP3', u'(VBD', u'ALLEGED', u'~VBD', u'(SBAR', u'(SBAR', u'(IN', u'THAT', u'~IN', u'(S', u'(NE', u'---', u'FRANCE', u'~NE', u'(VP4', u'(VBD', u'WAS', u'~VBD', u'(ADJP', u'(JJ', u'AWARE', u'~JJ', u'(PP', u'(IN', u'OF', u'~IN', u'(NE', u'---', u'PREPARATIONS', u'FOR', u'THE', u'GENOCIDE', u'~NE', u'~PP', u'~ADJP', u'~VP4', u'~S', u'~SBAR', u'(,', u',', u'~,', u'(CCP', u'AND', u'~CCP', u'(SBAR', u'(IN', u'THAT', u'~IN', u'(S', u'(NE', u'---', u'THE', u'FRENCH', u'MILITARY', u'IN', u'RWANDA', u'~NE', u'(VP5', u'(VBD', u'CONTRIBUTED', u'~VBD', u'(PP', u'(TO', u'TO', u'~TO', u'(S', u'(VP6', u'(VBG', u'PLANNING', u'~VBG', u'(NE', u'---', u'THE', u'MASSACRES', u'~NE', u'~VP6', u'~S', u'~PP', u'~VP5', u'~S', u'~SBAR', u'~SBAR', u'~VP3', u'(CCP', u'AND', u'~CCP', u'(VP7', u'(ADVP', u'(RB', u'ACTIVELY', u'~RB', u'~ADVP', u'(VBD', u'TOOK', u'~VBD', u'(NE', u'---', u'PART', u'IN', u'THE', u'KILLING', u'~NE', u'~VP7', u'~VP2', u'(.', u'.', u'~.', u'~S', u'~']
    sent = """( (S
            (NP (NP (DT A) (JJ 500-page) (NN report))
            (VP (VBN released)
            (NP (NNP Tuesday))
            (PP (IN in)
            (NP (DT the) (NNP Rwandan) (NN capital)))))
            (VP
            (VP (VBD alleged) (SBAR (SBAR (IN that) (S
            (NP (NNP France))
            (VP (VBD was) (ADJP (JJ aware)
            (PP (IN of)
            (NP (NP (NNS preparations))
            (PP (IN for)
            (NP (DT the) (NN genocide))))))))) (, ,) (CC and) (SBAR (IN that) (S
            (NP (NP (DT the) (JJ French) (NN military))
            (PP (IN in)
            (NP (NNP Rwanda))))
            (VP (VBD contributed)
            (PP (TO to) (S
            (VP (VBG planning)
            (NP (DT the) (NNS massacres)))))))))) (CC and)
            (VP (ADVP (RB actively)) (VBD took)
            (NP (NP (NN part))
            (PP (IN in)
            (NP (DT the) (NN killing)))))) (. .)))"""

    sent = utilities._format_parsed_str(sent)


    plist, pstart = petrarch.read_TreeBank(sent)
    assert plist == list and pstart == 2










