import torch.nn.functional as F
import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-small')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-small')
model.eval()

def average_pool(last_hidden_states, attention_mask):
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def get_embedding(text):
    with torch.no_grad():
        batch = tokenizer(text, padding=True, truncation=True, max_length=512, return_tensors="pt")

        outputs = model(**batch)
        embeddings = average_pool(outputs.last_hidden_state, batch["attention_mask"])

        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.detach().cpu().numpy()[0].tolist()


