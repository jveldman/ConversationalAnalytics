requirements.txt: 
	pigar generate
	cp requirements.txt requirements.lock

venv: 
	python -m venv .venv
	.\.venv\Scripts\activate
	pip intsall -r requirements.txt

install: venv
	pip install -e .

clean: 
	rm -rf __pychache__
	rm -rf .venv
	rm *.egg-info