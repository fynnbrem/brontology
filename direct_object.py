def extract_direct_object_relation(verb):
   for child in verb.children:
            # Überprüfen Sie, ob die Beziehung ein direktes Objekt ist
            if child.dep_ == "dobj":
                # Extrahieren Sie die Beziehung und fügen Sie sie der Liste hinzu
                results.append([sentence, verb.text, child.dep_, child.text])
