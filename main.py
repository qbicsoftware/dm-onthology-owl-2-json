# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from owlready2 import *
import json

global_class_dict = {}
found_classes = []


def first_from_list_or_null(a_list):
    try:
        return a_list[0] if len(a_list) > 0 else None
    except ValueError as exp:
        print(exp)
        print(a_list)


def extract_is_a_relation(onto_class):
    try:
        for is_a_class in onto_class.is_a:
            print(isinstance(is_a_class, Restriction))
            if isinstance(is_a_class, Restriction):
                class_entry = try_restriction_class_access(is_a_class)
            else:
                class_entry = try_class_access(is_a_class)
            found_classes.append(class_entry)
            global_class_dict[is_a_class.name] = is_a_class

    except Exception:
        print("Failed to access is_a relation in " + onto_class.name)


def try_restriction_class_access(restriction):
    onto_class = restriction.value
    try:
        # if onto.name not in onto_class.name.lower():
        #    return None
        class_entry_dict = {
            "label": first_from_list_or_null(onto_class.label),
            "name": onto_class.name,
            "IRI": onto_class.iri,
            "description": first_from_list_or_null(onto_class.IAO_0000115)
        }
        extract_is_a_relation(onto_class)
        return class_entry_dict
    except AttributeError:
        print("Cannot access properties for class " + onto_class.name)
        return None


def try_class_access(onto_class):
    try:
        # if onto.name not in onto_class.name.lower():
        #    return None
        class_entry_dict = {
            "label": first_from_list_or_null(onto_class.label),
            "name": onto_class.name,
            "IRI": onto_class.iri,
            "description": first_from_list_or_null(onto_class.IAO_0000115)
        }
        extract_is_a_relation(onto_class)
        return class_entry_dict
    except AttributeError:
        print("Cannot access properties for class " + onto_class.name)
        return None


def extract_class_attributes(onto_class):
    class_entry_dict = {
        "label": first_from_list_or_null(onto_class.label),
        "name": onto_class.name,
        "IRI": onto_class.iri,
        "description": first_from_list_or_null(onto_class.IAO_0000115)
    }
    return class_entry_dict


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Please provide the IRI of an ontology")
        exit(1)

    ontology_iri = sys.argv[1]
    print("Loading ontology " + ontology_iri)

    # ADO Alzheimer Disease Ontology
    # onto = get_ontology("https://raw.githubusercontent.com/Fraunhofer-SCAI-Applied-Semantics/ADO/main/ado.owl")
    # onto = get_ontology("https://raw.githubusercontent.com/Planteome/plant-ontology/master/po.owl")
    # onto = get_ontology("https://raw.githubusercontent.com/BRENDA-Enzymes/BTO/master/bto.owl")

    onto_path.append("./ontologies")
    onto = get_ontology(ontology_iri)

    onto.load()

    ontology_dict = {
        "ontology_name": onto.name,
        "ontology_base_iri": onto.base_iri,
        "ontology_title": onto.name,
        "ontology_version_info": onto.metadata.versionInfo[0] if len(onto.metadata.versionInfo) > 0 else None,
        "classes": []
    }

    print("Parsing ontology classes for " + onto.name + "...")
    total_classes = len(list(onto.classes()))
    processed_classes = 0
    for onto_class in onto.classes():
        processed_classes += 1
        print(f'Parsing class {processed_classes} of {total_classes} ({processed_classes / total_classes})\r')
        print(f'Class name: {onto_class.name}')
        class_entry = try_class_access(onto_class)
        if class_entry is None:
            continue
        found_classes.append(class_entry)

    found_classes_cleaned = [i for i in found_classes if i is not None and i['label'] is not None]

    for found_class in found_classes_cleaned:
        ontology_dict.get("classes").append(found_class)

    output = open(f'ontology_{onto.name}.json', "w")

    print("Writing ontology in JSON to output...")

    json.dump(ontology_dict, output, indent=4)

    print(f'Processed {len(found_classes_cleaned)} classes.')
