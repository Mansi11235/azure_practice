import azure.functions as func
import datetime
import json
import logging
import csv
import tempfile

app = func.FunctionApp()

@app.function_name('FirstFunction')
@app.route(route='hello')
def index(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('First functions started')
    return func.HttpResponse(
        'Hello World',
        status_code=200
    )

@app.route(route="demoTriggerFunc", auth_level=func.AuthLevel.ANONYMOUS)
def demoTriggerFunc(req: func.HttpRequest) -> func.HttpResponse:
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
    

@app.function_name(name='ReadfromBlobStorage')
@app.blob_trigger(arg_name="readFile",
                  path='demo-hogwarts/conversion.json',
                  connection='AzureWebJobsStorage')
@app.blob_output(arg_name="outputblob",
                path="demo-hogwarts/converted/converted.csv",
                connection="AzureWebJobsStorage")
def main(readFile: func.InputStream, outputblob: func.Out[str]):
    data = json.load(readFile)
    logging.info(readFile)
    # dir_path = tempfile.gettempdir()
    data_file = open(f'temp/conversion.csv', 'w')
    data_file.close()
    data_file = open(f'temp/conversion.csv', 'r+')
    csv_writer = csv.writer(data_file)
    count = 0
    for row in data['data']:
        if count == 0:
            # Writing headers of CSV file
            header = row.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(row.values())
    outputblob.set(data_file.read())
    