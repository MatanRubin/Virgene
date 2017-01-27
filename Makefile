PROJECT_NAME=virgene

all: checkstyle mypy test

test:
	pytest

coverage:
	pytest --cov=${PROJECT_NAME}

checkstyle:
	pep8 .

fixstyle:
	autopep8 --in-place -r .

mypy:
	mypy .


.PHONY: all test coverage checkstyle fixstyle mypy
