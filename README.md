<h1 align="center"> 💻 YouTube Comments Clustering 👾 </h1>
<p align="center"> An NLP project to cluster YouTube comments on the basis of their similarity of words </p>

##

#### Note
Sample raw data available along with processed data and images 

### Requirements

> It's preferable to install the requirements in a separate virtual environment

```bash
pip install -r requirements.txt
```
```bash
python
>>> import nltk
>>> nltk.download('stopwords')
```
```bash
python -m spacy download en_core_web_sm
```

### Usage

```bash
python -m venv project-venv
```

```bash
project-venv/Scripts/Activate
```
> Windows

```bash
source myenv/bin/activate
```
> Unix/Linux/Mac

<br>

```bash
cd "~/YT-Comments-Clustering"
```

```bash
python main.py
```