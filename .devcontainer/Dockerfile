
FROM --platform=linux/amd64 continuumio/miniconda3

# Turn on colors for ls
RUN echo "alias ls='ls --color=auto'" >> /root/.bashrc

RUN apt update

# Mecab stuff
RUN apt-get install -y mecab-ipadic-utf8
RUN conda install conda-forge::mecab-python3 conda-forge::unidic-lite -y
# Pandas
RUN conda install pandas -y

