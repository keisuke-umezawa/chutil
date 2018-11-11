.PHONY:	jupyter format_black build dist

IMAGE_NAME=alpacadb/alpaca-containers:forecast-exp-v0.0.2

MAKEFILE_PATH := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))
PROJECT_ROOT := $(abspath $(MAKEFILE_PATH))

DOCKER_OPTS=\
	--env-file $(PROJECT_ROOT)/.env \
	-e PYTHONPATH=/project/src

_mount_src:
	docker rm -f mysrc || echo
	docker create -v /project --name mysrc alpine:3.4 /bin/true
	docker cp $(PROJECT_ROOT)/. mysrc:/project/

mypy: _mount_src
	docker pull lloydmeta/mypy:python-3.5_latest
	docker run -it -w /project --volumes-from mysrc \
		--entrypoint mypy \
		lloydmeta/mypy:python-3.5_latest \
		--ignore-missing-imports --strict-optional --disallow-untyped-defs --disallow-untyped-calls /project/src

check_black: _mount_src
	docker pull unibeautify/black
	docker run -it -w /project --volumes-from mysrc \
		--entrypoint black \
		unibeautify/black \
		--line-length 88 --check /project

format_black:
	docker pull unibeautify/black
	docker run -it -v $(PROJECT_ROOT):/workdir -w /workdir unibeautify/black --line-length 88 /workdir

unittest: _mount_src
	docker run $(DOCKER_OPTS) \
		-it --volumes-from mysrc \
		$(IMAGE_NAME) \
		bash -c 'PYTHONIOENCODING=UTF-8 py.test $(UNIT_TEST_OPTS)'

build:
	python setup.py build

dist:
	rm -r dist
	python setup.py sdist

upload:
	twine upload dist/*

jupyter:
	bash -c "PYTHONPATH=`pwd`/src:${PYTHONPATH} jupyter notebook"
