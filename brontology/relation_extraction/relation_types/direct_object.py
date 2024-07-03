from brontology.relation_extraction.model import TokenRelation


def extract_direct_object_relation(verb):
    # Initialisiere das Subjekt und das direkte Objekt mit "NONE"
    dobj = None
    subj = None

    # Durchlaufe die Kinder des Verbs
    for child in verb.children:
        # Überprüfe, ob die Beziehung ein direktes Objekt ist
        if child.dep_ == "dobj":
            dobj = child
        # Überprüfen, ob die Beziehung ein Subjekt ist
        elif child.dep_ in ["nsubj"]:
            subj = child
    if dobj is None:
        return None
    if subj is None:
        return None

    return TokenRelation(subj, verb, dobj)
