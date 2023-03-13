import torch
import torch.nn as nn

class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super(SelfAttention, self).__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads

        assert (self.head_dim * heads == embed_size), "Embed size need to div by heads"

        self.values = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.keys = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.queries = nn.Linear(self.head_dim, self.head_dim, bias=False)
        self.fc_out = nn.Linear(heads*self.head_dim, embed_size)
    
    def forward(self, values, keys, queries, mask):
        N = queries.shape[0]
        value_len, key_len, querie_len = values.shape[1], keys.shape[1], queries.shape[1]

        # Split emb into self.heads  pic
        values = values.reshape(N, value_len, self.heads, self.head_dim)
        keys = keys.reshape(N, key_len, self.heads, self.head_dim)
        queries = queries.reshape(N, querie_len, self.heads, self.head_dim)

        values = self.values(values)
        keys = self.keys(keys)
        queries = self.queries(queries)

        energy = torch.einsum("nqhd,nkhd->nhqk" [queries, keys])

        if mask is not None:
            energy = energy.masked_fill(mask == 0, float("-1e20"))
        attention = torch.softmax(energy / (self.embed_size ** (1/2)), dim=3)

        out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(
            N, querie_len, self.heads*self.head_dim
        )

        out = self.fc_out(out)
        return out
    

class TransformerBlock(nn.Module):
    def __init__(self, embed_size, heads, dropout, forward_expension):
        super(TransformerBlock, self).__init__()
        self.attention = SelfAttention(embed_size, heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)

        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, forward_expension*embed_size),
            nn.ReLU(),
            nn.Linear(forward_expension*embed_size, embed_size)
        )

        self.dropout = nn.Dropout(dropout)
    
    def forward(self, values, keys, queries, mask):

        attention = self.attention(values, keys, queries, mask)
        x = self.dropout(self.norm1(attention + queries))
        forward = self.feed_forward(x)
        out = self.dropout(self.norm2(forward + x))

        return out 

class Encoder(nn.Module):
    def __init__(self, 
                 src_vocal_size, 
                 embed_size, 
                 num_layers, 
                 heads, 
                 device, 
                 forward_expension, 
                 dropout,
                 max_len
                 ):
        super(Encoder, self).__init__()
        self.embed_size = embed_size
        self.device = device
        self.word_emb = nn.Embedding(src_vocal_size, embed_size)
        self.pos_emb = nn.Embedding(max_len, embed_size)

        self.layers = nn.ModuleList(
            [
                TransformerBlock(embed_size=embed_size, 
                                 heads=heads, 
                                 dropout=dropout,
                                 forward_expension=forward_expension
                                 )
            for _ in range(num_layers)
            ]
        )
        self.dropout = nn.Dropout(dropout)
    def forward(self, x, mask):
        N, seq_len = x.shape
        position = torch.arange(0, seq_len).expand(N, seq_len).to(self.device)

        out = self.dropout(self.word_emb(x) + self.pos_emb(position))
        for layer in self.layers:
            out = layer(out, out, out, mask)
        
        return out
    
class DecoderBlock(nn.Module):
    def __init__(self, emb_size, heads, forward_expension, dropout, device):
        super(Decoder, self).__init__()
        self.attention = SelfAttention(emb_size, heads)
        self.norm = nn.LayerNorm(emb_size)
        self.transformer_block = TransformerBlock(
            emb_size, heads, dropout, forward_expension
            )
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, value, key, src_mask, target_mask):
        attantion = self.attention(x, x, x, target_mask)
        query = self.dropout(self.norm(attantion + x)) 
        out = self.transformer_block(value, key, query, src_mask)
        return out
    
class Decoder(nn.Module):
    def __init__(self,
                 trg_vocab_size, 
                 emb_size,
                 num_layers,
                 heads,
                 forward_expension,
                 dropout,
                 device,
                 max_len
                 ):
        super(Decoder, self).__init__()
        self.device = device
        self.word_emb = nn.Embedding(trg_vocab_size, emb_size)
        self.pos_emb = nn.EmbeddingBag(max_len, emb_size)

        self.layers = nn.ModuleList(
            [DecoderBlock(emb_size, heads, forward_expension, dropout, device) for _ in range(num_layers)]            
        )
        self.fc_out = nn.Linear(emb_size, trg_vocab_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, enc_out, src_mask, trg_mask):
        N, seq_len = x.shape
        position = torch.arange(0, seq_len).expand(N, seq_len).to(self.device)
        x = self.dropout(self.word_emb(x) + self.pos_emb(position))
        for layer in self.layers:
            x = layer(x, enc_out, enc_out, src_mask, trg_mask) 

        out = nn.fc_out(x)
        return out
    
class Transformer(nn.Module):
    def __init__(self, 
                 src_vocab_size,
                 trg_vocab_size,
                 scr_pad_idx,
                 trg_pad_idx,
                 embed_size=256, 
                 num_layers=6,
                 forward_expension=4,
                 heads=8,
                 dropout=0,
                 device="cuda",
                 max_len=100):
        
        super(Transformer, self).__init__()
        
        self.encoder = Encoder(src_vocal_size=src_vocab_size,
                               embed_size=embed_size,
                               num_layers=num_layers,
                               heads=heads,
                               device=device,
                               forward_expension=forward_expension,
                               dropout=dropout,
                               max_len=max_len)
        
        self.decoder = Decoder(trg_vocab_size=trg_vocab_size,
                               emb_size=embed_size,
                               num_layers=num_layers,
                               heads=heads,
                               device=device,
                               forward_expension=forward_expension,
                               dropout=dropout,
                               max_len=max_len)  
        
        self.src_pad_idx = scr_pad_idx
        self.trg_pad_idx = trg_pad_idx
        self.device = device

    def make_source_mask(self, src):
        src_mask = (src != self.src_pad_idx).unsqueeze(1).unsqueeze(2)
        return src_mask.to(self.device)
    
    def make_trg_mask(self, target):
        N, target_len = target.shape
        target_mask = torch.tril(torch.ones((target_len, target_len))).expand(
            N, 1, target_len, target_len
        )
        return target_mask.to(self.device)
    
    def forward(self, src, trg):
        src_mask = self.make_source_mask(src)
        target_mask = self.make_trg_mask(trg)
        enc_src = self.encoder(src, src_mask)
        out = self.decoder(trg, enc_src, src_mask, target_mask)
        return out

if __name__ == "__main__":
    device = "cpu"
    x = torch.tensor([[1,5,6,4,6,3,4,7,2],[3,6,4,8,1,2,7,4,0]]).to(device)
    trg = torch.tensor([[4,6,3,7,5,3,7,9],[3,5,1,7,3,5,8,2]]).to(device)

    src_pad_idx = 0
    trg_pad_idx = 0
    scr_vocal_size = 10
    trg_vocal_size = 10
    
    model = Transformer(scr_vocal_size, trg_vocal_size, src_pad_idx, trg_pad_idx).to(device)
    out = model(x, trg[:,:-1])

    print(out.shape)



























