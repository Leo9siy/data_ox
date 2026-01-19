# Test Task for DataOX

### App for Scratch Data from Site

with using PostgreSQL, Async Session and Docker

## How to start
1. clone repository
2. cd (repository)
3. change .env file
4. start project
```commandline
docker-compose up --build
```

```
├── docker-compose.yml     
├── Dockerfile          
├── src/                      # Main File
│   ├── works/                # Основной модуль с задачами Celery
│   ├── database/             # Database module
│   ├── dumps/                # Dir with dumps
│   ├── config.py             # App settings
│   ├── parse.py              # Main file
│   ├── scripts/              # Dir with scripts
│   ├── file_manager/         # Dir with work with files
│   └── .env                  # File with Environment variables
├── requirements.txt          # Requirements
└── README.md 
```

## In Steps

Start -> works (main -> tasks) -> parse.py -> scripts (parser -> collector)
-> file_manager (dump_data) -> dumps/ -> Finish
