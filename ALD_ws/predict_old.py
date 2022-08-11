import transformers
from transformers import XLMRobertaModel, XLMRobertaTokenizer, AdamW, get_linear_schedule_with_warmup

import torch
import pandas as pd
from torch import nn

class Predictor():

    def __init__(self, model):
        self.seed_value = 42
        self.seed_everything()
        self.class_names = ['not', 'prof']
        self.MODEL_NAME = 'xlm-roberta-large' 
        self.MAX_LEN = 128
        self.model = model
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print('Device : ', self.device)
        self.tokenizer = XLMRobertaTokenizer.from_pretrained(self.MODEL_NAME)


    def seed_everything(self):
        torch.manual_seed(self.seed_value)
        torch.cuda.manual_seed(self.seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True

    def load_model(self, model_path="./"):
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model = self.model.to(self.device)

    def predict(self, text):

        # text = 'senin beynini kuşlara taksak kuşlar geri geri uçar'

        print('Pred Tex2:', text)

        encoded_text = self.tokenizer(
          text,
          max_length=self.MAX_LEN,
          add_special_tokens=True,
          return_token_type_ids=False,
          pad_to_max_length=True,
          return_attention_mask=True,
          return_tensors='pt',
        )

        input_ids = encoded_text['input_ids'].to(self.device)
        attention_mask = encoded_text['attention_mask'].to(self.device)

        output = self.model(input_ids, attention_mask)
        _, prediction = torch.max(output, dim=1)


        print(f'Text: {text}')
        print(f'Profanity  : {self.class_names[prediction]}')
        print(f'Output: ', output)



class profanityDetectionClassifier(nn.Module):
    def __init__(self):
        super(profanityDetectionClassifier, self).__init__()
        self.seed_value = 42
        self.seed_everything()
        self.MODEL_NAME = 'xlm-roberta-large' 
        self.DROPOUT_RATE = 0.3
        self.xlmroberta = XLMRobertaModel.from_pretrained(self.MODEL_NAME)
        self.drop = nn.Dropout(p=self.DROPOUT_RATE)
        self.out = nn.Linear(self.xlmroberta.config.hidden_size, len(['not', 'prof']))

    def seed_everything(self):
        torch.manual_seed(self.seed_value)
        torch.cuda.manual_seed(self.seed_value)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = True


    def forward(self, input_ids, attention_mask):
        pooled_output = self.xlmroberta(
            input_ids=input_ids,
            attention_mask=attention_mask
            )
        output = self.drop(pooled_output.pooler_output)
        return self.out(output)