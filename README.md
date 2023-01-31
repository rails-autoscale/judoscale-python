# judoscale-python

This is the official Python adapter for [Judoscale](https://elements.heroku.com/addons/judoscale). You can use Judoscale without it, but this gives you request queue time metrics and job queue time (for supported job processors).

## Installation

Add judoscale-python to your <code>requirements.txt</code> file or the equivalent:

```
judoscale-python >= 1.0.0rc1
```

Then run this from a terminal to install the package:

```sh
pip install -r requirements.txt
```

## Supported web frameworks

- [x] Django
- [x] Flask
- [ ] FastAPI

## Supported job processors

- [ ] Celery
- [ ] RQ

## Using Judoscale with Django

Add Judoscale app to `settings.py`:

```python
INSTALLED_APPS = [
    "judoscale.django",
    # ... other apps
]
```

This sets up the Judoscale middleware to capture request queue times.

Optionally, you can customize Judoscale in `settings.py`:

```python
JUDOSCALE = {
    # LOG_LEVEL defaults to ENV["LOG_LEVEL"] or "INFO".
    "LOG_LEVEL": "DEBUG",

    # API_BASE_URL defaults to ENV["JUDOSCALE_URL"], which is set for you when you install Judoscale.
    # This is only exposed for testing purposes.
    "API_BASE_URL": "https://example.com",

    # REPORT_INTERVAL_SECONDS defaults to 10 seconds.
    "REPORT_INTERVAL_SECONDS": 5,
}
```

Once deployed, you will see your request queue time metrics available in the Judoscale UI.

# Using Judoscale with Flask

The Flask support for Judoscale is packaged into a Flask extension. Import the extension class and use like you normally would in a Flask application:


```py
# app.py

from judoscale.flask import Judoscale

# If your app is a top-level global

app = Flask("MyFlaskApp")
app.config.from_object('...')  # or however you configure your app
judoscale = Judoscale(app)


# If your app uses the application factory pattern

judoscale = Judoscale()

def create_app():
    app = Flask("MyFlaskApp")
    app.config.from_object('...')  # or however you configure your app
    judoscale.init_app(app)
    return app
```

This sets up the Judoscale extension to capture request queue times.

Optionally, you can override Judoscale's own configuration via your application's [configuration dictionary](https://flask.palletsprojects.com/en/2.2.x/api/#flask.Flask.config). The Judoscale Flask extension looks for a top-level `"JUDOSCALE"` key in `app.config`, which should be a dictionary, and which the extension uses to configure itself as soon as `judoscale.init_app()` is called.

```python
JUDOSCALE = {
    # LOG_LEVEL defaults to ENV["LOG_LEVEL"] or "INFO".
    "LOG_LEVEL": "DEBUG",

    # API_BASE_URL defaults to ENV["JUDOSCALE_URL"], which is set for you when you install Judoscale.
    # This is only exposed for testing purposes.
    "API_BASE_URL": "https://example.com",

    # REPORT_INTERVAL_SECONDS defaults to 10 seconds.
    "REPORT_INTERVAL_SECONDS": 5,
}
```

Note the [official recommendations for configuring Flask](https://flask.palletsprojects.com/en/2.2.x/config/#configuration-best-practices).

# Using Judoscale with Celery and Redis

> **NOTE:** The Judoscale Celery integration currently only works with the [Redis broker](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html#redis).

Judoscale can automatically scaling the number of Celery workers based on the queue latency (the age of the oldest pending task in the queue).

To use the Celery integration, import `judoscale_celery` and pass it the Celery "app" instance as the last step, after setup and configuration.

```py
from celery import Celery
from judoscale.celery import judoscale_celery

broker = Celery("Broker", broker="redis://localhost:6379/0")
# Further setup
# broker.conf.update(...)
# ...

judoscale_celery(broker)
```

This sets up Judoscale to periodically calculate and report queue latency for each Celery queue.

Note that the queue names are captured via the [`before_task_publish` signal](https://docs.celeryq.dev/en/latest/userguide/signals.html#before-task-publish) and stored in the metrics collector.

If you need to change any config options, you can pass a dictionary of Judoscale configuration options to override the default Judoscale config variables:

```py
judoscale_celery(broker, extra_config={"LOG_LEVEL": "DEBUG"})
```

## Development

This repo includes a `sample-apps` directory containing apps you can run locally. These apps use the judoscale-python adapter, but they override `API_BASE_URL` so they're not connected to the real Judoscale API. Instead, they post API requests to https://requestcatcher.com so you can observe the API behavior.

See the `README` in a sample app for details on how to set it up and run locally.

### Contributing

`judoscale-python` uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging the project. Head over to the [installations instructions](https://python-poetry.org/docs/#installing-with-the-official-installer) and install Poetry, if needed.

Clone the repo with

```sh
$ git clone git@github.com:judoscale/judoscale-python.git
$ cd judoscale-python
```

Verify that you are on a recent version of Poetry:

```sh
$ poetry --version
Poetry (version 1.3.1)
```

Install dependencies with Poetry and activate the virtualenv

```sh
$ poetry install
$ poetry shell
```

Run tests with

```sh
$ python -m unittest discover -s tests
```
