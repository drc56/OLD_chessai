setup:
	pip install --user virtualenv
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/python3 -m pytest -v test

lint:
	black pychess_ai/ test/

clean:
	rm -rf venv
	find -iname "*.pyc" -delete

.PHONY: test lint