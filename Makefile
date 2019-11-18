
default:
	pip install -e .[develop]

publish: clean
	python setup.py bdist_wheel
	twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

backend:
	docker-compose run --rm --service-ports backend bash
