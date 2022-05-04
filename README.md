# Dall-E Alchemist

## About
This repo contains our code for generating images using Dall-E mini for our game "The Dall-E Alchemist".

## Dependencies
It is recommended to create a virtual environment with the following packages:
```
pip install -q git+https://github.com/huggingface/transformers.git
pip install -q git+https://github.com/patil-suraj/vqgan-jax.git
pip install -q git+https://github.com/borisdayma/dalle-mini.git
```

## References
This [notebook](https://colab.research.google.com/github/borisdayma/dalle-mini/blob/main/tools/inference/inference_pipeline.ipynb#scrollTo=uzjAM2GBYpZX) was used as a reference from this code. This [repo](https://github.com/borisdayma/dalle-mini) is the official Dall-E Mini repo.

## TODO:
- Set up pipeline for generating and saving image outputs from text input
- Create a set of words to be used as input
- Generate all possible combination
- Generate images from the combinations
- Save combinations in an easy to access way
