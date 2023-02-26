import json
import logging
import os

import torch
from transformers import BertTokenizer
from json import JSONEncoder
import numpy as np

logger = logging.getLogger(__name__)

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class BertMultiClassHandler(object):

    def __init__(self):
        super(BertMultiClassHandler, self).__init__()
        self.manifest = None
        self.tokenizer = None
        self.initialized = False
        self.model = None
        self.device = 'cuda'

    def initialize(self, context):
        properties = context.system_properties
        self.manifest = context.manifest

        model_dir = properties.get("model_dir")
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)

        self.tokenizer = BertTokenizer.from_pretrained('sberbank-ai/ruBert-large', model_max_length=64)
        self.model = torch.jit.load(model_pt_path).to(self.device)
        self.initialized = True
        
    def _get_preprocessed(self, sentence):
        
        encoded_dict = self.tokenizer.encode_plus(
            sentence, 
            add_special_tokens=True, 
            truncation=True,
            max_length=64, 
            padding='max_length',
            return_tensors='pt', 
            return_attention_mask = True
        )
        return encoded_dict

    def preprocess(self, requests):
        
        input_ids_batch = None
        attention_mask_batch = None      
        
        for idx, data in enumerate(requests):            
            input_text = data.get("data")
            if input_text is None:
                input_text = data.get("body")
            if isinstance(input_text, (bytes, bytearray)):
                input_text = input_text.decode("utf-8")
            inputs = self._get_preprocessed(input_text)
            
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)

            if input_ids.shape is not None:
                if input_ids_batch is None:
                    input_ids_batch = input_ids
                    attention_mask_batch = attention_mask
                else:
                    input_ids_batch = torch.cat((input_ids_batch, input_ids), 0)
                    attention_mask_batch = torch.cat((attention_mask_batch, attention_mask), 0)
                    
        return input_ids_batch, attention_mask_batch

        
    def inference(self, input_batch):

        input_ids_batch, attention_mask_batch = input_batch

        with torch.no_grad():
            logits = self.model(input_ids_batch, attention_mask_batch)
            
        logits = torch.softmax(logits, dim=1)
        logits = logits.detach().cpu().numpy()
        return logits

    def postprocess(self, data):
        dumped_data = [json.dumps(d.tolist()) for d in data]
        return dumped_data


_service = BertMultiClassHandler()


def handle(data, context):
    if not _service.initialized:
    
        _service.initialize(context)
    
    if data is None:
        return None

    data = _service.preprocess(data)
    data = _service.inference(data)
    data = _service.postprocess(data)
    return data