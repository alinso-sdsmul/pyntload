import requests
import base64
import json
import sys,imp

#headers to use
headers = {
        "Accept": "application/json,text/javascript,*/*",
        'Authorization': 'Bearer dapi03fa57be956e3d0a07a050177327334d-2',
        "Content-Type": "application/json"
}

#base url
base_url = "https://adb-7118152657858843.3.azuredatabricks.net/"

def init_module(module_name):
    
    #create new module
    mymodule = imp.new_module(module_name)

    return mymodule

def read_databricks_notebook(notebook_path):
    
    #get module
    module = init_module('test')
    
    #get notebook export
    response = requests.request(
        "GET",
        base_url + "api/2.0/workspace/export",
        headers =headers,
        params= {
            'path': notebook_path,
            'format': 'JUPYTER'
        }
    )
    
    #parse python code (json to dict)
    jupyter_code = json.loads(base64.b64decode(response.json()["content"]))
    jupyter_code_cells = [cell for cell in jupyter_code["cells"] if cell["cell_type"]=="code"]
    jupyter_code_cells = [''.join(cell['source']) for cell in jupyter_code_cells]
    
    return '\n'.join(jupyter_code_cells)
    
    '''
    #for each code cell, add to module
    for code_cell in jupyter_code_cells:
        
        #join to get code
        code = ''.join(code_cell['source'])
        
        #exec code
        exec(code, module.__dict__)
        
    return module
    '''