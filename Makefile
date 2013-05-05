PROJ := peloid
LIB := $(PROJ)
GITHUB_REPO := github.com:oubiwann/$(PROJ).git
TMP_FILE ?= /tmp/MSG
VIRT_DIR ?= .venv
PYTHON_BIN ?= /System/Library/Frameworks/Python.framework/Versions/2.7/bin
PYTHON ?= $(PYTHON_BIN)/python2.7
PYTHON ?= $(shell env python)
VERSION ?= $(shell $(PYTHON) -c "from peloid import meta; print meta.version;")
PACKAGE_NAME ?= $(shell $(PYTHON) -c "from peloid import meta; print meta.display_name;")
PACKAGE_EXT ?= tar.gz
VENV ?= .venv
ACT ?= $(VENV)/bin/activate
TEST_VENV ?= .venv-test
TEST_ACT ?= $(TEST_VENV)/bin/activate
KEY_DIR ?= $(shell . $(ACT) && python -c "from peloid import config;print config.ssh.keydir;")

$(KEY_DIR):
	. $(ACT) && twistd peloid keygen

$(VENV):
	virtualenv $(VENV)

$(TEST_VENV):
	virtualenv $(TEST_VENV)

generate-game-file:
	# this make target needs to take game data files and create a custom zip
	# file that can be loaded with "twistd peloid --game-file=filename"
	echo

deps:
	. $(ACT) && pip install carapace
	. $(ACT) && pip install txmongomodel

run: $(VENV) $(KEY_DIR) deps
	@clear
	@. $(ACT) && twistd -n peloid

daemon: $(VENV) $(KEY_DIR) deps
	@clear
	@echo "Starting daemon ..."
	@. $(ACT) && twistd peloid

shell: $(VENV) $(KEY_DIR)
	@clear
	@echo "Starting shell ..."
	@. $(ACT) && ssh -o StrictHostKeyChecking=no -p 4222 127.0.0.1

telnet:
	@telnet localhost 4221

stop:
	@echo "Stopping daemon ..."
	@kill `cat twistd.pid`

test-run:
	make daemon && make shell && make stop

version:
	@echo $(VERSION)

banner: SUB_DIR ?= test-build
banner: DIR ?= $(VIRT_DIR)/$(SUB_DIR)
banner:
	@. $(DIR)/bin/activate && python -c "from peloid import config; print config.ssh.banner;"


generate-config: $(ENV)
	@. $(ACT) && python -c "from peloid import app;from carapace.sdk import scripts;scripts.GenerateConfig();"

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

todo:
	git grep -n -i -2 XXX
	git grep -n -i -2 TODO
.PHONY: todo

build:
	$(PYTHON) setup.py build
	$(PYTHON) setup.py sdist

check: $(TEST_VENV) test-deps build
	@clear
	@. $(TEST_ACT) && trial $(LIB)

test-deps:
	. $(TEST_ACT) && pip install carapace
	. $(TEST_ACT) && pip install txmongomodel

clean-check:
	rm -rf $(TEST_VENV)

full-check: clean-check $(TEST_VENV) test-deps build
	. $(TEST_ACT) && trial $(LIB)

register:
	$(PYTHON) setup.py register

upload: check
	$(PYTHON) setup.py sdist upload --show-response