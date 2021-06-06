![develop](https://github.com/mrinmoyghosal/devnet/actions/workflows/ci.yml/badge.svg)

## Developer Connected API

This application finds if the provided usernames are connected or not. 
Given a pair of developer handles they are considered connected if:
* They follow each other on Twitter.
* They have at least a Github organization in common.

### Assumptions
* Assume that people having the same handle both in Twitter and Github are actually the same
person. 

*  `/api/v1/connected/register/<dev1>/<dev2>` and `/api/v1/connected/register/<dev2>/<dev1>` will return same result


### Installations


* Dependencies
   * Python 3.9
   * pip & pipenv
   
* Set environment variables
```shell script
# Twitter Credentials
export TWITTER_CONSUMER_KEY = <tw_consumer_key>
export TWITTER_CONSUMER_SECRET = <tw_consumer_secret>
export TWITTER_ACCESS_TOKEN = <twitter_access_token>
export TWITTER_ACCESS_TOKEN_SECRET = <tw_access_token_secret>

# Github Credentials
export GITHUB_ACCESS_TOKEN = <your_github_access_token>
```
   
* Install and run
```shell script
# install pipenv
pip install pipenv

# run the web app
cd devnet
pipenv install

# apply migrations
pipenv flask db upgrade 
pipenv run python wsgi.py
```

* Install and Run via Docker
```shell script
cd devnet

# pass your environement vars in key and val
docker build -t devnetapi .
docker run -p 5000:5000 --env ENV_KEY=ENV_VAL --name devnetapp devnetapi 
```

* Run flake8 
```
flake8 app
```

* Run pylint 
```
pylint --fail-under 10 --load-plugins pylint_flask_sqlalchemy app
```
* Run Tests 
```
pytest --rootdir app --disable-warnings
```

#### Endpoints

- Realtime API
```
/api/v1/connected/realtime/<dev1>/<dev2>
```
- Realtime API Response
```
{
  "connected": false,
  "organisations": [
    "string"
  ]
}
```

- Historical API

```
/api/v1/connected/register/<dev1>/<dev2>
```
- Historical API Response
```
{
  "data": [
    {
      "connected": false,
      "organisations": [
        "string"
      ],
      "registered_at": "2021-06-06T01:08:42.488Z"
    }
  ]
}
```

- Swagger Doc
```
/api/v1/
```

