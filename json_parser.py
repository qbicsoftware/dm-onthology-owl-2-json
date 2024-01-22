import json


def parse_json(path):
    ontology = json.load(open(path))
    output = {
        "ontology_name": "NCBITaxon",
        "ontology_base_iri": "http://purl.obolibrary.org/obo/ncbitaxon.owl",
        "ontology_title": "An ontology representation of the NCBI organismal taxonomy",
        "ontology_version_info": "http://purl.obolibrary.org/obo/ncbitaxon/2023-09-19/ncbitaxon.owl",
        "classes": []
    }

    for term in ontology['graphs'][0]['nodes']:
        if term['type'] != "CLASS":
            continue
        ontology_class = {
            "label": term['lbl'],
            "name": term['id'].split("/")[-1],
            "IRI": term['id'],
            "description": None
        }
        output['classes'].append(ontology_class)

    with open("ontology_ncbitaxon.json", "w") as fp:
        json.dump(output, fp, indent=4)


if __name__ == '__main__':
    parse_json("obo/ncbitaxon.json")
