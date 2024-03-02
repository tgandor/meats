#!/usr/bin/env python

import argparse
import time

try:
    from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
except ImportError:
    print("Install requirements:")
    print("pip install torch torchvision torchaudio transformers sentencepiece protobuf")

parser = argparse.ArgumentParser()
parser.add_argument("--list", action="store_true")
parser.add_argument("--source", "-f", default="en")
parser.add_argument("--target", "-t", default="pl_PL")
parser.add_argument("--cuda", action="store_true")
args = parser.parse_args()

tokenizer = MBart50TokenizerFast.from_pretrained(
    "facebook/mbart-large-50-many-to-many-mmt"
)

if args.list:
    print("Output languages:")
    print(", ".join(tokenizer.lang_code_to_id.keys()))
    print("For input language, skip country suffix.")
    exit()

model = MBartForConditionalGeneration.from_pretrained(
    "facebook/mbart-large-50-many-to-many-mmt"
)

if args.cuda:
    encoded = model.to("cuda")
    print("Using CUDA")

tokenizer.src_lang = args.source

while True:
    msg = input(f"{args.source}> ")
    if not msg:
        break
    print("please wait...", end="\r")
    start = time.time()
    encoded = tokenizer(msg, return_tensors="pt")
    if args.cuda:
        encoded = encoded.to("cuda")
    generated_tokens = model.generate(
        **encoded, forced_bos_token_id=tokenizer.lang_code_to_id[args.target]
    )
    print(
        f"{args.target}:",
        tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0],
    )
    print(f"(generated in {time.time() - start:.3f} s)")
