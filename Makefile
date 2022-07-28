install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

mac-install:
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt


run:
	python index.py

mac-run:
	python3 index.py

format:
	python -m black ./*.py ./views/core/*.py ./views/page/*.py ./models/*.py ./utilities/*.py

lint:
	python -m pylint ./*.py ./views/core/*.py ./views/page/*.py ./models/*.py ./utilities/*.py

db-init:
	flask db init

db-upgrade:
	flask db upgrade