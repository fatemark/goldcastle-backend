cmake_minimum_required(VERSION 3.18)
project(atwar)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)

# Set include directories for libpqxx
include_directories(include /opt/homebrew/Cellar/libpqxx/7.9.0/include)

# Add source files
add_executable(AtWar src/main.cpp)

# Link libpqxx with your executable
target_link_libraries(AtWar PRIVATE /opt/homebrew/Cellar/libpqxx/7.9.0/lib/libpqxx-7.9.dylib)
