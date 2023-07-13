ifneg (,$(wildcard .env))
    $(info Found .env file.)
    include .env
    export
endif

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

style: 
    flake8 webapp


types:
    mypy webapp

tests:
    pytest --lf -vv .

check:
    make style types tests