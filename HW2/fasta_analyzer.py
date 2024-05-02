import re
import requests
import json
from Bio import SeqIO
import subprocess

# HW 2_1

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
def database_match(inp: list):
    seq = list()
    fasta = dict()
    description = dict()
    for i in inp:
        seq += [re.search(r'(?<=\|).*(?=\|)', str(i.id)).group()]
        fasta[seq[-1]] = i.seq 
        description[seq[-1]] = i.description

    type_uniprot = all(re.fullmatch("[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", ID) for ID in seq)
    type_ensembl = all(re.fullmatch('(ENS[A-Z]{0,3}|MGP_[a-zA-Z0-9]*_)[A-Z]{1,2}\d{11}', ID) for ID in seq)

    if type_uniprot:
        return "Protein", "UNIPROT", seq, description, fasta
    elif type_ensembl:
        return "DNA", "ENSEMBL", seq, description, fasta
    else:
        return ValueError("Wrong format"), "Error", seq, description, fasta

def database_explorer(inp: list):

    # I have finally found uniprot.org/help/accession_numbers and re-visit ensembl.org/info/genome/stable_ids/prefixes.html, so now it should finally work) My regex was the same with the regex on the site.

    type_uniprot = bool(re.fullmatch("[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}", inp))
    type_ensembl = bool(re.fullmatch('(ENS[A-Z]{0,3}|MGP_[a-zA-Z0-9]*_)[A-Z]{1,2}\d{11}', inp))

    if type_uniprot:
        vals = get_uniprot([inp])
        res = uniprot_parse_response(vals)

        for i in [inp]:
            print(i)
            print('organism:', res[i]['organism'])
            print('geneInfo:', res[i]['geneInfo'])
            print('sequenceInfo', res[i]['sequenceInfo'])
            print('type:', res[i]['type'], "\n")
        return "UNIPROT", res
    elif type_ensembl:
        vals = get_ensembl([inp])
        res = ensembl_parse_response(vals)
        
        for i in [inp]:
            print(i)
            print('organism:', res[i]['organism'])
            print('geneInfo:', res[i]['geneInfo'])
            print('sequenceInfo', res[i]['sequenceInfo'])
            print('type:', res[i]['type'], "\n")
        return "ENSEMBL", res
    else:
        return "ERROR", ValueError("Wrong format")

# HW 2_2
def seqkit_call(path):
    #path = "hw_file1.fasta"

    seqkit = subprocess.run(("seqkit", "stats", path, "-a"),
                            capture_output=True,
                            text=True)
    
    #catch error
    if seqkit.stderr != "":
        return ("Catched error: ", seqkit.stderr)
    else:
        tmp = seqkit.stdout.split()
        t2 = (len(tmp)//2)
        tmp1 = tmp[0:t2]
        tmp2 = tmp[t2:len(tmp)]
        tmp = dict()
        for i in zip(tmp1, tmp2):
            print(i[0], "\t", i[1])
            tmp[i[0]] = i[1]

        return(tmp['type'])

def biopython_parser(path):
    path = "hw_file1.fasta"
    sequences = SeqIO.parse(path, "fasta")

    d1, d2, seq, description, fasta = database_match(sequences)

    if (d2 == "ERROR"):
        print("Error occured; please check input format")
    else:
        res = dict()
        res["seqkit"] = seqkit_call(path)
        tmp_seqs = dict()
        for s in seq:
            tmp_s = dict()
            tmp_s["description"]  = description[s]
            tmp_s["fasta"] = fasta[s]
            tmp_s["DB_name"], tmp_s["DB_info"] = database_explorer(s)
            tmp_seqs[s] = tmp_s

        res["seqs"] = tmp_seqs
        print(res)
        return(res)


# TEST SYSTEM
inp = input("Write path to fasta: ").split()
for i in inp:
    biopython_parser(i)
