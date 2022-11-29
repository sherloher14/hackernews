import graphene
from graphene_django import DjangoObjectType
import requests
import base64
import io
import json
import numpy as np

from PIL import Image

LINEAR_SERVER_URL = 'https://linear-model-service-ivanjvr.cloud.okteto.net/v1/models/linear-model:predict'

RESNET_SERVER_URL = 'https://resnet-service-ivanjvr.cloud.okteto.net/v1/models/resnet:predict'



class Query(graphene.ObjectType):
    linear_predictions = graphene.String(values=graphene.String())
    resnet_predictions = graphene.String(photourl=graphene.String())


    def resolve_linear_predictions(self, info, values,  **kwargs):
        predict_request = '{"instances" : [ %s ]}' % values
        print (predict_request)
        response = requests.post(LINEAR_SERVER_URL, data=predict_request)
        response.raise_for_status()
        prediction = response.json()
        print (prediction['predictions'])
        return prediction['predictions']

    def resolve_resnet_predictions(self, info, photourl,  **kwargs):
        IMAGE_URL = photourl
        dl_request = requests.get(IMAGE_URL, stream=True)
        dl_request.raise_for_status()

        jpeg_rgb = Image.open(io.BytesIO(dl_request.content))

        # Normalize and batchify the image
        jpeg_rgb = np.expand_dims(np.array(jpeg_rgb) / 255.0, 0).tolist()
        #predict_request = json.dumps({'instances': jpeg_rgb})
        jpeg_bytes = base64.b64encode(dl_request.content).decode('utf-8')

        predict_request = '{"instances" : [{"b64": "%s"}]}' % jpeg_bytes 

        #print (predict_request)
        response = requests.post(RESNET_SERVER_URL, data=predict_request)
        response.raise_for_status()
        #prediction = response.json()['predictions']
        prediction = response.json()['predictions'][0]['classes']
        print(prediction)
        return prediction

