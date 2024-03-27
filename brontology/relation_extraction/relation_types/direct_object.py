def extract_direct_object_relation(verb):
    # Initialisiere das Subjekt und das direkte Objekt mit "NONE"
    dobj = "NONE"
    subj = "NONE"

    # Durchlaufe die Kinder des Verbs
    for child in verb.children:
        # Überprüfe, ob die Beziehung ein direktes Objekt ist
        if child.dep_ == "dobj":
            dobj = child.text
        # Überprüfen, ob die Beziehung ein Subjekt ist
        elif child.dep_ in ["nsubj", "nsubjpass"]:
            subj = child.text

    # Füge das direkte Objekt und das Subjekt der Liste hinzu, unabhängig davon, ob sie gefunden wurden oder nicht
    results.append([verb.sent, verb.text, dobj, subj])