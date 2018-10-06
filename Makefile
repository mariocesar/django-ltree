

default: clean
	./venv/bin/python setup.py bdist_wheel
	./venv/bin/twine upload dist/*

clean:
	rm -rf dist/
	rm -rf build/

