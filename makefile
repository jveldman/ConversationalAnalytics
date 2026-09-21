requirements.txt: 
	pigar generate
	cp requirements.txt requirements.lock

venv: 
	python -m venv .venv
	.\.venv\Scripts\activate
	pip install -r requirements.txt

install: venv
	pip install -e .

clean: 
	rm -rf __pychache__
	rm -rf .venv
	rm *.egg-info

run_dev:
	cd ingestion && pocca-ingest --db dev
	cd pocca && dbt build --target dev && dbt compile
	cd cube-core && ./sync_cubes.sh && docker-compose down && docker-compose up -d  

run_prod: 
	cd ingestion && pocca-ingest --db prod
	cd pocca && dbt build --target prod && dbt compile
	
