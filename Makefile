
style: 
	flake8 .

types:
	mypy .

tests:
	pytest --lf -vv .

check:
	make style types tests
