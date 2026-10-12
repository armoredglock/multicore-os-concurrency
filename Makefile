CC = gcc
CFLAGS = -Wall -Wextra -O2 -pthread
TSAN_FLAGS = -Wall -Wextra -O2 -fsanitize=thread -pthread
BIN_DIR = bin

SRC_M1 = src/module1_concurrency_race_conditions
SRC_M2 = src/module2_deadlock_and_bankers

TARGETS = $(BIN_DIR)/race_condition $(BIN_DIR)/mutex_sync $(BIN_DIR)/semaphore_sync $(BIN_DIR)/spinlock_atomic_sync

all: $(BIN_DIR) $(TARGETS)

$(BIN_DIR):
	mkdir -p $(BIN_DIR)

$(BIN_DIR)/race_condition: $(SRC_M1)/race_condition.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/mutex_sync: $(SRC_M1)/mutex_sync.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/semaphore_sync: $(SRC_M2)/semaphore_sync.c
	$(CC) $(CFLAGS) $< -o $@

$(BIN_DIR)/spinlock_atomic_sync: $(SRC_M2)/spinlock_atomic_sync.c
	$(CC) $(CFLAGS) $< -o $@

# Target for ThreadSanitizer (supported on Linux/POSIX hosts)
tsan: $(SRC_M1)/race_condition.c
	$(CC) $(TSAN_FLAGS) $< -o $(BIN_DIR)/race_tsan

# Target for Disassembly and Interleaving Trace Analysis
disasm:
	python scripts/disassemble_race.py

clean:
	rm -rf $(BIN_DIR) *.exe *.o

.PHONY: all clean tsan disasm
