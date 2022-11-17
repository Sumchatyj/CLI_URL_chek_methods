# CLI_URL_chek_methods

## Description

This is a CLI script for checking http methods by URL. it took 8 hours to complete the job.


## Getting started

### Dependencies

* Python > 3.7
* aiohttp == 3.8.3
* pytest == 7.2.0

### Installing

Make your own venv:

```
python3 -m venv venv
```

Activate:

```
source venv/bin/activate
```

Install requirements:

```
pip install -r requirements.txt
```

Start the script:

```
python cli.py ["testing URL"]
```

### Tests

The script is fully covered with tests:

```
pytest --cov=cli
```

The result:

![Alt text](coverage.png?raw=true "Coverage")
