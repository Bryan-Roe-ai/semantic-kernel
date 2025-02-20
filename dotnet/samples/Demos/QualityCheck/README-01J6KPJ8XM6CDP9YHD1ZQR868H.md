---
runme:
  document:
    relativePath: README.md
  session:
    id: 01J6KPJ8XM6CDP9YHD1ZQR868H
    updated: 2024-08-31 07:56:45Z
---

# Quality Check with Filters

This sample provides a practical demonstration how to perform quality check on LLM results for such tasks as text summarization and translation with Semantic Kernel Filters.

Metrics used in this example:

- [BERTScore](ht*********************************re) - leverages the pre-trained contextual embeddings from BERT and matches words in candidate and reference sentences by cosine similarity.
- [BLEU](ht******************************EU) (BiLingual Evaluation Understudy) - evaluates the quality of text which has been machine-translated from one natural language to another.
- [METEOR](ht********************************OR) (Metric for Evaluation of Translation with Explicit ORdering) - evaluates the similarity between the generated summary and the reference summary, taking into account grammar and semantics.
- [COMET](ht***************************ET) (Crosslingual Optimized Metric for Evaluation of Translation) - is an open-source framework used to train Machine Translation metrics that achieve high levels of correlation with different types of human judgments.

In this example, SK Filters call dedicated [server](./python-server/) which is responsible for task evaluation using metrics described above. If evaluation score of specific metric doesn't meet configured threshold, an exception is thrown with evaluation details.

[Hugging Face Evaluate Metric](ht***********************************te) library is used to evaluate summarization and translation results.

## Prerequisites

1. [Python 3.12](ht****************************ds/)
2. Get [Hugging Face API token](ht*********************************************************************en).
3. Accept conditions to access [Unbabel/wm**************da](ht*********************************************da) model on Hugging Face portal.

## Setup

It's possible to run Python server for task evaluation directly or with Docker.

### Run server

1. Open Python server directory:

```bash {"id":"01J6KPZDAVF1X7Y4QPQ8GPRYBZ"}
cd python-server
```

2. Create and active virtual environment:

```bash {"id":"01J6KPZDAVF1X7Y4QPQAH8GW5P"}
python -m venv venv
source venv/Scripts/activate # activate on Windows
source venv/bin/activate # activate on Unix/MacOS
```

3. Setup Hugging Face API key:

```bash {"id":"01J6KPZDAVF1X7Y4QPQBEAVCPK"}
pip install "huggingface_hub[cli]"
huggingface-cli login --token <your_token>
```

4. Install dependencies:

```bash {"id":"01J6KPZDAVF1X7Y4QPQEFZW3XM"}
pip install -r requirements.txt
```

5. Run server:

```bash {"id":"01J6KPZDAVF1X7Y4QPQJ854X21"}
cd app
uvicorn main:app --port 8080 --reload
```

6. Open `ht**********************cs` and check available endpoints.

### Run server with Docker

1. Open Python server directory:

```bash {"id":"01J6KPZDAVF1X7Y4QPQKK2C1YH"}
cd python-server
```

2. Create following `Dockerfile`:

```dockerfile {"id":"01J6KPZDAVF1X7Y4QPQPQPEEHC"}
# sy*********er/do******le:1.2
FROM py**on:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install "huggingface_hub[cli]"
RUN --mount=type=secret,id=hf_token \
    huggingface-cli login --token $(cat /run/secrets/hf_token)

RUN pip install cmake
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

3. Create `.env/hf_token.txt` file and put Hugging Face API token in it.
4. Build image and run container:

```bash {"id":"01J6KPZDAVF1X7Y4QPQTE7XAKN"}
docker-compose up --build
```

5. Open `ht**********************cs` and check available endpoints.

## Testing

Open and run `QualityCheckWithFilters/Program.cs` to experiment with different evaluation metrics, thresholds and input parameters.
