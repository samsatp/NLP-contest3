
def extract_sentences_from_files(files):
    sentences = []
    sentence = []
    for f in files:
        for line in open(f, encoding="utf8"):
            if line == '\n':
                sentences.append(sentence)
                sentence = []
            else:
                token, pos_tag, ner_tag, _  = line.strip().split('\t')
                sentence.append((token if token != '_' else ' ', ner_tag, pos_tag))
    return sentences


def extract_entities(sentence, post=False):
    """Extract entities from a sentence

    a sentence should be a list of tuples like this
    [
        ('ล่าสุด', 'O', pos)
        (' ', 'O')
        ('เบ็น', 'B_ORG')
        ('คิว', 'I_ORG')
        (' ', 'O')
        ('ได้', 'O')
        ('ให้', 'O')
        ('ความ', 'O')
        ('สำคัญ', 'O')
        ('กับ', 'O')
        ('เน็ตบุ๊ค', 'O')
    ]
    
    This will return [('ORG, 'เบ็นคิว')]
    """

    entities = []
    entity_sofar = []
    type_sofar = None
    tokens = []
    for s in sentence:
        if not post:
            token, ner_tag, _ = s
        else:
            token, ner_tag = s
        tokens.append(token)
        if ner_tag[0] == 'B':
            if type_sofar is not None:
                entities.append((type_sofar, ''.join(entity_sofar)))
                entity_sofar = []
                type_sofar = None
            if len(ner_tag) > 1:
                _, tag = ner_tag.split('_')
                type_sofar = tag
                entity_sofar.append(token)
            else:
                type_sofar = 'MISC'
                entity_sofar.append(token)
            
        elif ner_tag[0] == 'I':
            if len(ner_tag) > 1:
                _, tag = ner_tag.split('_')
                type_sofar = tag
            entity_sofar.append(token)
        elif ner_tag[0] == 'E':
            entity_sofar.append(token)
            entities.append((type_sofar, ''.join(entity_sofar)))
            entity_sofar = []
            type_sofar = None
        elif ner_tag == 'O':
            if len(entity_sofar) != 0:
                entities.append((type_sofar, ''.join(entity_sofar)))
                entity_sofar = []
                type_sofar = None
    return ''.join(tokens), [(t, x) for t, x in entities if t is not None]

def retag(entities, tokens, pos):
    e_list = entities.copy()
    if len(e_list) == 0:
        return list(zip(tokens, ['O' for _ in range(len(tokens))], pos))
    ent_type, entity = e_list.pop(0)
    pointer = 0
    tags = []
    for i, token in enumerate(tokens):
        idx = entity.find(token, pointer)
        if idx == pointer and idx == 0:
            tags.append('B_{}'.format(ent_type))
            pointer = idx + len(token)
        elif idx == pointer:
            tags.append('I_{}'.format(ent_type))
            pointer = idx + len(token)
        else:
            tags.append('O')
        if pointer == len(entity):
            pointer = 0
            if len(e_list) > 0:
                ent_type, entity = e_list.pop(0)
            else:
                break

    for j in range(i+1, len(tokens)):
        tags.append('O')

    
    assert(len(tags)==len(tokens)==len(pos))
    return list(zip(tokens,tags, pos))

