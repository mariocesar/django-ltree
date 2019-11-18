
default:
	pip install -e .[develop]
	cd example && pip install -r requirements.txt

publish: clean
	python setup.py bdist_wheel
	twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

backend:
	docker-compose run --rm --service-ports backend --shell
