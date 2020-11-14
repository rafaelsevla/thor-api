## Getting Started

### Clone project, create virtual env, install dependencies and active virtual env

```
git clone git@github.com:rafaelsevla/thor-api.git
cd thor-api
```
```
python3 -m venv .venv or virtualenv -p python3 .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```


### Add token on .env

```
echo WEATHER_API_TOKEN=PUT_YOUR_TOKEN_HERE > .env
```

or copy .env.example and put token manually in file:
```
cp .env.example .env
```

### Run project:
```
flask run
```


### Endpoints:
```
[ GET ] /city?id=(id_from_advisor)
[ POST ] /city?id=(id_from_advisor)&days=(amount_days)
[ GET ] /analyze?initial_date=(date)&finish_date=(date)
```