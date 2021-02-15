import os, pandas, csv, re
import numpy as np
from biothings.utils.dataload import dict_convert, dict_sweep

from biothings import config
logging = config.logger

def load_reactome(data_folder):
    infile = os.path.join(data_folder,"reactome.homo_sapiens.interactions.tab-delimited.txt")
    assert os.path.exists(infile)
    dat = pandas.read_csv(infile,sep="\t",squeeze=True,quoting=csv.QUOTE_NONE).to_dict(orient='records')
    results = {}
    id_ctr = 0
    for rec in dat:
        _id = id_ctr
        id_ctr = id_ctr + 1
        # we'll remove space in keys to make queries easier. Also, lowercase is preferred
        # for a BioThings API. We'll an helper function from BioThings SDK
        process_key = lambda k: k.replace(" ","_").lower()
        rec = dict_convert(rec,keyfn=process_key)
        # remove NaN values, not indexable
        rec = dict_sweep(rec,vals=[np.nan])
        results.setdefault(_id,[]).append(rec)
        
    for _id,docs in results.items():
        doc = {"_id": _id, "annotations" : docs}
        yield doc
