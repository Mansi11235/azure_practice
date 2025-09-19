import azure.functions as func
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="store_to_blob_trigger", auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_output(arg_name="outputblob",
                path="<blob storage name>/test.json",
                connection="AzureWebJobsStorage")
def store_to_blob_trigger(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request. Blob Storage output')

    # logging.info(f'Python blob storing')
    outputblob.set(json.dumps({"name": "harry"}))
    return "ok"
    

    

@app.route(route="dummy", auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_output(arg_name="outputblob",
                path="anushkawalmartb8cf/test2.json",
                connection="AzureWebJobsStorage")
def BlobStore(req: func.HttpRequest, outputblob: func.Out[str]) -> func.HttpResponse:
    logging.info(f'Python blob storing')
    outputblob.set(json.dumps({"name": "harry"}))
    return "ok"