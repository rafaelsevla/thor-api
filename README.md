## Getting Started

### Create virtual env, install dependencies and active virtual env


```
virtualenv -p python3 .venv
```
```
pip install -r requirements.txt
```
```
source .venv/bin/activate
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
[ GET ] /city?id=(id_from_advisor)
[ POST ] /city?id=(id_from_advisor)&days=(amount_days)
[ GET ] /analyze?initial_date=(date)&finish_date=(date)