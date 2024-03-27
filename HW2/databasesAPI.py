import re
import requests
import json

# UNIPROT
def get_uniprot(ids: list):
    accessions = ','.join(ids)
    endpoint = "https://rest.uniprot.org/uniprotkb/accessions"
    http_function = requests.get
    http_args = {'params': {'accessions': accessions}}
    return http_function(endpoint, **http_args)


def uniprot_parse_response(resp: dict):
    resp = resp.json()
    resp = resp["results"]
    output = {}
    for val in resp:
        acc = val['primaryAccession']
        species = val['organism']['scientificName']
        gene = val['genes']
        seq = val['sequence']
        output[acc] = {'organism': species, 'geneInfo': gene,
                       'sequenceInfo': seq, 'type': 'protein'}

    return output

# ENSEMBL
def get_ensembl(ids: list):
    endpoint = 'https://rest.ensembl.org/lookup/id'
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}
    return requests.post(endpoint, headers=headers, data=json.dumps({'ids': ids}))


def ensembl_parse_response(resp: dict):
    resp = resp.json()
    output = {}
    for inp in resp.items():
        acc = inp[0]
        val = inp[1]
        species = val['species']

        if "display_name" in val:
            gene = val['description']
        elif "description" in val:
            gene = val['description']
        else:
            gene = NameError

        seqtype = val['object_type']  

        pos = {'assembly_name': val['assembly_name'],
               "start":val['start'], 
               "end": val['end']}
        
        output[acc] = {'organism': species, 'geneInfo': gene,
                       'sequenceInfo': pos, 'type': seqtype}
        
    return output

# Get database query
def database_explorer(inp: list):
    type_uniprot = all(re.fullmatch("[A-Z]\w{5}|\w{7}|\w{9}", ID) for ID in inp)
    type_ensembl = all(re.fullmatch('(ENS[A-Z]{0,3}|MGP_[a-zA-Z]*_)\w\w?\d{11}', ID) for ID in inp)

    if type_uniprot:
        vals = get_uniprot(inp)
        res = uniprot_parse_response(vals)

        for i in inp:
            print(i)
            print('organism:', res[i]['organism'])
            print('geneInfo:', res[i]['geneInfo'])
            print('sequenceInfo', res[i]['sequenceInfo'])
            print('type:', res[i]['type'], "\n")
        return(res)
    elif type_ensembl:
        vals = get_ensembl(inp)
        res = ensembl_parse_response(vals)
        
        for i in inp:
            print(i)
            print('organism:', res[i]['organism'])
            print('geneInfo:', res[i]['geneInfo'])
            print('sequenceInfo', res[i]['sequenceInfo'])
            print('type:', res[i]['type'], "\n")
        return(res)
    else:
        return ValueError("Wrong format")
        
        
inp = input("Write database IDs:").split()
database_explorer(inp)
