import torch
import os
from ..BaseNER import BaseNER
from ....utils.seq_dataloader import SeqDataset
from ....nn.models import BertLSTMCRF
from ....data import load


class BertNER(BaseNER):
    def __init__(self, device=None):
        self.ner_path = load('ner')
        self.model = BertLSTMCRF(input_size=300, hidden_size=200, label_sizes=[8], toplayer='CRF')
        self.seq = SeqDataset(tag_path=os.path.join(self.ner_path, 'tagset.txt'),
                              bert_tokenizer='bert-base-chinese')
        self.id2tag = self.seq.tagging()
        self.checkpoint = torch.load(os.path.join(self.ner_path, "bert2.pth"), map_location=lambda storage, loc: storage)
        self.model.load_state_dict(self.checkpoint['net'], False)
        self.model.eval()

        super().__init__(device)

    def to(self, device):
        self.model.to(device)
        return super().to(device)

    def __call__(self, sents):
        results = []
        for sent in sents:
            test_pkg = {'token': sent, 'tag': ' '.join(['O'] * len(sent))}
            tokens, tags, masks = self.seq.transformer.item2id(test_pkg)
            tokens = torch.LongTensor([tokens])
            with torch.no_grad():
                out = self.model.predict(8, tokens.to(self.device), masks.to(self.device))
                out = out.cpu().tolist()[0]
                print(out)
                out_etts = self.get_entity(out, self.id2tag)
            results.append(out_etts)
        return results

    def get_entity(self, path, tag_map):
        results = []
        record = {}
        for index, tag_id in enumerate(path):
            if tag_id == 0:
                continue
            tag = tag_map[tag_id]
            print(tag)
            if tag.startswith("B_"):
                if record.get("end"):
                    if record["type"] != "T":
                        results.append(record)
                record = {}
                record["begin"] = index
                record["type"] = tag.split("_")[1]
            elif tag.startswith("I_") and "begin" in record:
                tag_type = tag.split("_")[1]
                if tag_type == record["type"]:
                    record["end"] = index
            else:
                if record.get("end"):
                    if record["type"] != "T":
                        results.append(record)
                    record = {}
            print(record)
        if record.get("end"):
            if record["type"] == "T":
                pass
            else:
                results.append(record)
        return results