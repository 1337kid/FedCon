PROGRAM_NAME=fedcon
VERSION=1.1
DATA_DIR=/usr/share
PROGRAM_DIR=/usr/bin

install:
	install -Dm755 fedcon.py $(PROGRAM_DIR)/$(PROGRAM_NAME)
	mkdir -p $(PROGRAM_DIR)/fedconcore
	install -Dm644 fedconcore/* $(PROGRAM_DIR)/fedconcore
	mkdir -p $(DATA_DIR)/$(PROGRAM_NAME)
	install -Dm644 instances.txt $(DATA_DIR)/$(PROGRAM_NAME)/instances.txt

uninstall:
	rm -Rf $(PROGRAM_DIR)/$(PROGRAM_NAME)
	rm -Rf $(DATA_DIR)/$(PROGRAM_NAME)