# 1. Compiler and Paths
CC = clang
CFLAGS = -Wall -O3 -Xpreprocessor -fopenmp -I/opt/homebrew/opt/libomp/include
LDFLAGS = -lm -L/opt/homebrew/opt/libomp/lib -lomp

# 2. File and Directory Definitions
SRC_DIR = src/c
BUILD_DIR = build
TARGET_LIB = libquantum.dylib
TARGET_EXE = quantum_sim

# Every .c file in your src folder becomes a .o file in build
SRCS = $(SRC_DIR)/engine.c $(SRC_DIR)/gates.c
OBJS = $(BUILD_DIR)/engine.o $(BUILD_DIR)/gates.o

# 3. Default Rule (Builds both the lib for Python and the C executable)
all: $(BUILD_DIR) $(TARGET_LIB) $(TARGET_EXE)

# 4. Link the Dynamic Library (.dylib) for Python
$(TARGET_LIB): $(BUILD_DIR)/engine.o $(BUILD_DIR)/gates.o
	$(CC) -dynamiclib -o $@ $^ $(LDFLAGS)

# 5. Link the C Executable (for tests/debugging)
$(TARGET_EXE): $(OBJS) $(SRC_DIR)/main.c
	$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

# 6. Compile Source Files into Object Files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# 7. Utilities
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

clean:
	rm -rf $(BUILD_DIR) $(TARGET_LIB) $(TARGET_EXE)

run: all
	./$(TARGET_EXE)

.PHONY: all clean run