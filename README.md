# Souche Crawler

## Configuration

```shell
SITE_URL = 'https://souche.com/'
REGION = 'hangzhou'

LIST_URL = SITE_URL + REGION + '/list-pg{}'

FIRST_PAGE = 1

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36'

DB_URL = 'mysql+pymysql://haha:passwd1Q@127.0.0.1/fuck?charset=utf8'
```

## Run

```shell
$ pip install -r requirements.txt

$ python run.py
```

## Troubleshooting

**question: Incorrect string value**

```shell
sqlalchemy.exc.InvalidRequestError: This Session's transaction has been rolled back due to a previous exception during flush. To begin a new transaction with this Session, first issue Session.rollback(). Original exception was: (pymysql.err.InternalError) (1366, "Incorrect string value: '\\xE6\\xAC\\xBE  \\xE5...' for column 'name' at row 1"
```

**answer**

```sql
# set utf8 charaset

create database fuck   DEFAULT CHARACTER SET utf8  DEFAULT COLLATE utf8_general_ci;
```
