# Funnel Friction Map

See where people leave a sequential funnel and which cohorts account for the loss.

**[Open the live demo](https://oguzhanozfe.github.io/funnel-friction-map/)** · [Browser features and setup](demo/DEMO.md)

![Funnel Friction Map showing the included example in the browser](docs/preview.png)

[Deploy to Render](https://render.com/deploy?repo=https://github.com/oguzhanozfe/funnel-friction-map) · [Example input](example.json) · [Computed report](docs/example-report.json) · [Model settings](#connect-a-model)

## Try it

With Python 3.11 or newer, run:

```sh
git clone https://github.com/oguzhanozfe/funnel-friction-map.git
cd funnel-friction-map
python app.py
```

Open **http://127.0.0.1:8000**. The example is already loaded. Choose **Input JSON** to edit it or open your own file, then **Run analysis**. **Export report** saves the computed evidence as JSON. The example works on a CPU with no dependencies, accounts or API keys.

## What the example shows

## What this measures

Use Funnel Friction Map when a conversion rate has slipped and you need to choose a step to investigate. In the example, desktop and mobile visitors can both create a workspace. The important difference emerges when they invite a teammate. The table shows how many people actually reached that decision, how many progressed, and how many left.

Supply ordered stage names and a list of counts for each mutually exclusive cohort. Count each participant once per stage, use the same observation window, and give each cohort enough time to finish. For every transition the loss percentage divides people lost by the number entering that step. Overall completion pools people across cohorts. An empty denominator produces a blank rate.

The summary highlights the largest absolute loss across all cohorts, with the earliest stage breaking ties. A small group can still have the highest percentage loss. These aggregates cannot identify why someone stopped, distinguish a delayed event from a departure, or correct overlapping cohorts upstream.

**Sample result:** The largest pooled loss was 133 of 317 people from Created workspace to Invited teammate.

## Run without a browser

```sh
python app.py analyze example.json
python -m unittest discover -v
```

The CLI writes JSON to stdout. The HTTP interface accepts `POST /api/analyze` with content type `application/json` and body `{"input": {...}, "review": false}`. The input object has the same shape as [example.json](example.json). `GET /api/example` returns a complete working request input and report. `GET /health` is the deployment health check.

## Connect a model

Analysis always computes the measurements locally. To add an English review of those measurements, select a provider on the **server**, set its variables and restart. `MODEL_PROVIDER=off` is the default.

| Provider | Configuration |
| --- | --- |
| Local (Ollama, LM Studio, llama.cpp) | `MODEL_PROVIDER=local`, `MODEL_ID=<installed chat model>`, `MODEL_BASE_URL=http://127.0.0.1:11434/v1` (Ollama) or `http://127.0.0.1:1234/v1` (LM Studio). |
| Azure OpenAI | `MODEL_PROVIDER=azure`, `MODEL_ID=<deployment name>`, `MODEL_BASE_URL=https://<resource>.openai.azure.com/openai/v1`, `MODEL_API_KEY=<resource key>`. |
| AWS Bedrock | `MODEL_PROVIDER=bedrock`, `MODEL_ID=<Converse-compatible model or inference profile ID>`, `AWS_REGION=<region>`. Use an AWS role or the standard SDK credential chain with permission to invoke that model. Install `requirements.txt` when running outside Docker. |
| OpenAI or compatible hosted API | `MODEL_PROVIDER=api`, `MODEL_BASE_URL=https://<provider>/v1`, `MODEL_ID=<chat model>`, `MODEL_API_KEY=<key>`. The default API root is `https://api.openai.com/v1`. |

For example, with a running local model (Bash):

```sh
MODEL_PROVIDER=local MODEL_ID=your-model MODEL_BASE_URL=http://127.0.0.1:1234/v1 python app.py analyze example.json --review
```

On PowerShell set each variable with `$env:MODEL_ID = "your-model"` (and likewise for the provider and base URL) before running `python app.py analyze example.json --review`. Model output is a separate `model_review` field. The model receives the summary, metrics and a bounded sample of result rows. An optional review with a hosted provider sends that evidence to the configured provider.

## Deploy

The Render link uses [render.yaml](render.yaml) to deploy the included Dockerfile. Select the new service and deploy. An account is required on the hosting platform. To run the same container locally:

```sh
docker build -t funnel-friction-map .
docker run --rm -p 127.0.0.1:8000:8000 funnel-friction-map
```

The container honors `PORT` (default 8000). Add provider variables through the host's secret settings or Docker's `--env-file`. For browser model reviews on a deployment, also set a long `MODEL_ACCESS_TOKEN` and enter it in **Model review**. The server keeps provider credentials out of the browser. To reach a model on the Docker host, use a reachable host address instead of container loopback; Docker Desktop provides `host.docker.internal`.

The deterministic analysis lives in [project.py](project.py). Provider adapters are in [providers.py](providers.py). [MIT license](LICENSE).
