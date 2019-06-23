
default:
	cd example && pip install -r requirements.txt

publish: clean
	./venv/bin/python setup.py bdist_wheel
	./venv/bin/twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

backend:
	docker-compose run --rm --service-ports backend --shell
