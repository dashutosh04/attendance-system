import torchaudio
torchaudio.set_audio_backend("soundfile")

import torch
from speechbrain.pretrained import SpeakerRecognition

_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    run_opts={"device": "cpu"}
)

def get_embedding(audio):
    with torch.no_grad():
        return _model.encode_batch(
            torch.tensor(audio).unsqueeze(0)
        ).squeeze()

def similarity(a, b):
    return torch.nn.functional.cosine_similarity(a, b, dim=0).item()
