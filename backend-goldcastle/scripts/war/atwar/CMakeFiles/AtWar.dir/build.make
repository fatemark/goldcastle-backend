# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.28.3/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar

# Include any dependencies generated for this target.
include CMakeFiles/AtWar.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/AtWar.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/AtWar.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/AtWar.dir/flags.make

CMakeFiles/AtWar.dir/src/main.cpp.o: CMakeFiles/AtWar.dir/flags.make
CMakeFiles/AtWar.dir/src/main.cpp.o: src/main.cpp
CMakeFiles/AtWar.dir/src/main.cpp.o: CMakeFiles/AtWar.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/AtWar.dir/src/main.cpp.o"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/AtWar.dir/src/main.cpp.o -MF CMakeFiles/AtWar.dir/src/main.cpp.o.d -o CMakeFiles/AtWar.dir/src/main.cpp.o -c /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/src/main.cpp

CMakeFiles/AtWar.dir/src/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/AtWar.dir/src/main.cpp.i"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/src/main.cpp > CMakeFiles/AtWar.dir/src/main.cpp.i

CMakeFiles/AtWar.dir/src/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/AtWar.dir/src/main.cpp.s"
	/Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/src/main.cpp -o CMakeFiles/AtWar.dir/src/main.cpp.s

# Object files for target AtWar
AtWar_OBJECTS = \
"CMakeFiles/AtWar.dir/src/main.cpp.o"

# External object files for target AtWar
AtWar_EXTERNAL_OBJECTS =

AtWar: CMakeFiles/AtWar.dir/src/main.cpp.o
AtWar: CMakeFiles/AtWar.dir/build.make
AtWar: /opt/homebrew/Cellar/libpqxx/7.9.0/lib/libpqxx-7.9.dylib
AtWar: CMakeFiles/AtWar.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable AtWar"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/AtWar.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/AtWar.dir/build: AtWar
.PHONY : CMakeFiles/AtWar.dir/build

CMakeFiles/AtWar.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/AtWar.dir/cmake_clean.cmake
.PHONY : CMakeFiles/AtWar.dir/clean

CMakeFiles/AtWar.dir/depend:
	cd /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar /Users/esse/Desktop/crypto/gold_castle/nft/database_localhost/backend-goldcastle/scripts/war/atwar/CMakeFiles/AtWar.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/AtWar.dir/depend
