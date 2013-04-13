PROJ := dreammud
LIB := $(PROJ)
GITHUB_REPO := github.com:dreamhost/$(PROJ).git
PKG_NAME := $(PROJ)
TMP_FILE ?= /tmp/MSG
VIRT_DIR ?= .venv
PYTHON_BIN ?= /System/Library/Frameworks/Python.framework/Versions/2.7/bin
PYTHON ?= $(PYTHON_BIN)/python2.7

run:
	twistd -n dreammud

daemon:
	twistd dreammud

shell:
	-@ssh -p 4222 127.0.0.1

stop:
	kill `cat twistd.pid`

test-run:
	make daemon && make shell && make stop

banner:
	$(PYTHON) -c "from dreammud import config; print config.ssh.banner;"

generate-config:
	$(PYTHON) -c "from dreammud import app;from carapace.sdk import scripts;scripts.GenerateConfig();"

log-concise:
	git log --oneline

log-verbose:
	git log --format=fuller

log-authors:
	git log --format='%aN %aE' --date=short

log-authors-date:
	git log --format='%ad %aN %aE' --date=short

log-changes:
	git log --format='%ad %n* %B %N%n' --date=short

clean:
	find ./ -name "*~" -exec rm {} \;
	find ./ -name "*.pyc" -exec rm {} \;
	find ./ -name "*.pyo" -exec rm {} \;
	find . -name "*.sw[op]" -exec rm {} \;
	rm -rf _trial_temp/ build/ dist/ MANIFEST \
		CHECK_THIS_BEFORE_UPLOAD.txt *.egg-info

push:
	git push --all git@$(GITHUB_REPO)

push-tags:
	git push --tags git@$(GITHUB_REPO)

push-all: push push-tags
.PHONY: push-all

stat:
	@echo
	@echo "### Git info ###"
	@echo
	git info
	echo
	@echo "### Git working branch status ###"
	@echo
	@git status -s
	@echo
	@echo "### Git branches ###"
	@echo
	@git branch
	@echo 

status: stat
.PHONY: status

todo:
	git grep -n -i -2 XXX
	git grep -n -i -2 TODO
.PHONY: todo

build:
	$(PYTHON) setup.py build
	$(PYTHON) setup.py sdist

build-docs:
	cd docs/sphinx; make html

check-docs: files = "README.rst"
check-docs:
	@echo "noop"

check-examples: files = "examples/*.py"
check-examples:
	@echo "noop"

check-dist:
	@echo "Need to fill this in ..."

check: build check-docs check-examples
	trial $(LIB)

check-integration:
# placeholder for integration tests
.PHONY: check-integration

version:
	@echo $(VERSION)

virtual-build: SUB_DIR ?= test-build
virtual-build: DIR ?= $(VIRT_DIR)/$(SUB_DIR)
virtual-build: clean build
	mkdir -p $(VIRT_DIR)
	-test -d $(DIR) || virtualenv $(DIR)
	@. $(DIR)/bin/activate
	-test -e $(DIR)/bin/twistd || $(DIR)/bin/pip install twisted
	-test -e $(DIR)/bin/rst2html.py || $(DIR)/bin/pip install docutils
	$(DIR)/bin/pip uninstall -vy $(PKG_NAME)
	$(PYTHON_BIN)/easy_install-2.7 ./dist/$(PKG_NAME)*

clean-virt: clean
	rm -rf $(VIRT_DIR)

virtual-build-clean: clean-virt build virtual-build
.PHONY: virtual-build-clean

register:
	$(PYTHON) setup.py register

upload: check
	$(PYTHON) setup.py sdist upload --show-response
