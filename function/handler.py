
import json
import os
from flask import Request

from rdkit.Chem import AllChem as Chem
import numpy as np
import pandas as pd
from sklearn.externals import joblib

function_root = os.environ.get("function_root")

# load model
model = joblib.load('/home/app/chembl_25/models/10uM/mNB_10uM_all.pkl')
classes = list(model.targets)


def handle(req: Request):
    """handle a request to the function.

    Your response is immediately passed to the caller, unmodified.
    This allows you full control of the response, e.g. you can set
    the status code by returning a tuple (str, int). A detailed
    description of how responses are handled is found here:

    http://flask.pocoo.org/docs/1.0/quickstart/#about-responses

    Args:
        req (Request): Flask request object
    """
    # load molecule from smiles and calculate fp
    mol = Chem.MolFromSmiles(req.get_json()['smiles'])
    if mol:
        fp = Chem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
        fp = np.asarray(fp).reshape(1, -1)

        # predict
        data = zip(classes, model.predict_proba(fp)[0])
        predictions = pd.DataFrame(data, columns=['chembl_id', 'proba'])
        predictions = predictions.to_dict(orient='records')
    else:
        predictions = None
    return json.dumps(predictions)
