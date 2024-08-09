# Buy-The-Dip
Python class final project - web app

## Setup

Create virtual environment:

```sh
conda create -n dip-env python=3.11
```

Activate the environment

```sh
conda activate dip-env
```


Install packages:

```sh
# best practice to list the packages in the requirements.txt file
pip install -r requirements.txt
```

```sh
pip install -U kaleido # (for image chart)
```

Access API Key from ALPHAVANTAGE AND FinnHub API 
Also create a ".env" file in the root directory of the repo, and paste some contents in like this

## Usage

Run the script:

#  STARTS TO GET DIFFERENT 
stocks report:

```sh
python -m app.data

Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```


## Testing

Run tests:

```sh
pytest
```


