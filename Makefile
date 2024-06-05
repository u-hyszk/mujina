
PYTHON_VERSION := 3.10
PROJECT_NAME := mujina

.PHONY: mk_bulid_dir
mk_bulid_dir: ## Make the build directory
	mkdir -p build

.PHONY: cp_package
cp_package: ## Copy the package to the build directory
	cp -r ./.venv/lib/python$(PYTHON_VERSION)/site-packages/ ./build/

.PHONY: cp_src
cp_src: ## Copy the source to the build directory
	cp -r ./src/$(PROJECT_NAME)/ ./build/

$(PROJECT_NAME).zip: ## Create the zip file
	cd ./build && zip -r ../$(PROJECT_NAME).zip .

.PHONY: build
build:
	$(MAKE) mk_bulid_dir
	$(MAKE) cp_package
	$(MAKE) cp_src
	$(MAKE) $(PROJECT_NAME).zip