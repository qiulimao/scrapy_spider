# scrapy spider documentation

##usage
>	for user

before using this program,
you need to change some parameters
* DATABASE_URL in scrapy_spider/webspider/settings.py
* sqlalchemy.url in scrapy_spider/alembic.ini(if you are to using alembic)

### how to run it?

if you are the fist time to run this program

before run the program,you need to run the below command to create table in given database
```bash
python webspider/models.py
```


```bash
startspider.py --init
#or
# startspider.py -i
```

if you are to update the data use:
```bash
startspider.py --update
# or
# startspider.py -u
# o
# startspider.py
# by default the startspider.py run as update
```

## develop
> for program monkeys

place your update run spider in [timing_run] space

like this:

```
[timing_run]
seebug_updator = 1
wooyun_updator = 1
```
place your init run spider in [init_run] space

like this:

```python
[initial_run]
seebug = 1
wooyun = 1
```

# note
>   when use alembic to  manage database migrations,be careful,it may bite! if user database exists some tables, be CAREFUL,alembic may delete the tables!!!

# about me

* name   : qiulimao
* email  : qiulimao@getqiu.com
* website: http://www.getqiu.com
 
