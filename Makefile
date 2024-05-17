AUTHOR  := dwisiswant0
APP     := apkleaks
IMAGE   := $(AUTHOR)/$(APP)
VERSION := $(shell cat VERSION | tr -d '\n')
PACKAGE := $(APP)-$(shell echo $(VERSION) | cut -c 2-)

VENV := venv
PYTHON := python3
# PIP := pip3

ifneq ($(wildcard $(VENV)),)
	PYTHON = $(VENV)/bin/python3
	# PIP = $(VENV)/bin/pip3
endif

venv:
	python3 -m venv $(VENV)

setup:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install build twine

setup-venv: venv
setup-venv: PYTHON = $(VENV)/bin/python3
setup-venv: setup

build-package:
	@$(PYTHON) -m build

check-package:
	@$(PYTHON) -m twine check dist/$(PACKAGE)*

upload-package:
	@$(PYTHON) -m twine upload dist/$(PACKAGE)*

pypi: check-package build-package

build-images:
	@docker build -t $(IMAGE):latest .
	@docker tag $(IMAGE):latest $(IMAGE):$(VERSION)

upload-images:
	@docker push $(IMAGE):latest
	@docker push $(IMAGE):$(VERSION)

docker: build-images

build-all: build-package build-images

upload-all: upload-package upload-images

clean:
	@rm -rfv dist/ venv/
	@docker image rm -f dwisiswant0/apkleaks