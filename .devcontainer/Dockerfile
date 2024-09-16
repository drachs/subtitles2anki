
FROM --platform=linux/amd64 continuumio/miniconda3

# Turn on colors for ls
RUN echo "alias ls='ls --color=auto'" >> /root/.bashrc

RUN apt update && apt install -y vim less
RUN conda install -y conda-forge::mecab-python3 conda-forge::unidic-lite conda-forge::pykakasi pandas conda-forge::openai

