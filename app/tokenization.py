import spacy

nlp = spacy.load("en_core_web_lg")


def to_named_entities(text: str) -> None:
    doc = nlp(text)

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)
