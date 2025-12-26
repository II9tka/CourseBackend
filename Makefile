SHELL := /bin/bash

# --- Project root detection (folder name is CourseBackend) ---
PROJECT_NAME := CourseBackend
CWD := $(shell pwd -P)

PROJECT_DIR := $(shell echo "$(CWD)" | sed -n 's#^\(.*\/$(PROJECT_NAME)\)\(/.*\)\?$$#\1#p')
ifeq ($(strip $(PROJECT_DIR)),)
$(error "Can't find project root folder '$(PROJECT_NAME)' in current path: $(CWD)")
endif

SRC_DIR := $(PROJECT_DIR)/src

# Alembic config: prefer src/alembic.ini, fallback to project root alembic.ini
ALEMBIC_CFG := $(firstword $(wildcard $(SRC_DIR)/alembic.ini $(PROJECT_DIR)/alembic.ini))
ifeq ($(strip $(ALEMBIC_CFG)),)
$(error "Can't find alembic.ini in $(SRC_DIR) or $(PROJECT_DIR)")
endif

VERSIONS_DIR := $(SRC_DIR)/migrations/versions
ifeq ($(wildcard $(VERSIONS_DIR)),)
$(error "Can't find versions dir: $(VERSIONS_DIR)")
endif

# --- Params (support both short and long names) ---
# Usage examples:
#   make new m="init"
#   make up r=0007
#   make down r=0007
#   make down
MSG ?= $(m)
REV ?= $(r)

# --- Helpers ---
define next_rev_id
max=$$(ls -1 "$(VERSIONS_DIR)" 2>/dev/null | awk -F'_' '/^[0-9]+_/{print $$1}' | sort -n | tail -1); \
if [ -z "$$max" ]; then next=1; else next=$$((10#$$max + 1)); fi; \
printf "%04d" $$next
endef

# --- Info ---
.PHONY: where
where:
	@echo "PROJECT_DIR=$(PROJECT_DIR)"
	@echo "SRC_DIR=$(SRC_DIR)"
	@echo "ALEMBIC_CFG=$(ALEMBIC_CFG)"
	@echo "VERSIONS_DIR=$(VERSIONS_DIR)"

# --- New command set ---
# make new m="message"   -> create migration with auto numeric rev-id
.PHONY: new
new:
	@if [ -z "$(MSG)" ]; then \
		echo 'Usage: make new m="message"'; \
		echo '   or: make new MSG="message"'; \
		exit 2; \
	fi
	@rev="$$( $(call next_rev_id) )"; \
	echo "Creating migration rev-id=$$rev, message='$(MSG)'"; \
	cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" revision --autogenerate -m "$(MSG)" --rev-id "$$rev"

# make up            -> upgrade head
# make up r=0007     -> upgrade to specific revision (inclusive)
.PHONY: up
up:
	@if [ -n "$(REV)" ]; then \
		echo "Upgrading to revision $(REV)"; \
		cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" upgrade "$(REV)"; \
	else \
		echo "Upgrading to head"; \
		cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" upgrade head; \
	fi

# make down          -> downgrade base
# make down r=0007   -> downgrade to specific revision
.PHONY: down
down:
	@if [ -n "$(REV)" ]; then \
		echo "Downgrading to revision $(REV)"; \
		cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" downgrade "$(REV)"; \
	else \
		echo "Downgrading to base"; \
		cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" downgrade base; \
	fi

# --- Keep other commands (as before) ---
.PHONY: current history heads
current:
	@cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" current

history:
	@cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" history --verbose

heads:
	@cd "$(SRC_DIR)" && alembic -c "$(ALEMBIC_CFG)" heads

# Backward-compatible alias (if you had it)
.PHONY: makemigrations
makemigrations: new
