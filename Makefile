
default:
	pip install -e .[develop]

build: clean
	python -m build -s -w

publish: build
	twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

backend:
	docker-compose run --rm --service-ports backend bash
