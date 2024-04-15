# Locate libpqxx
find_path(libpqxx_INCLUDE_DIR pqxx/pqxx /opt/homebrew/Cellar/libpqxx/7.9.0/include)
find_library(libpqxx_LIBRARY pqxx /opt/homebrew/Cellar/libpqxx/7.9.0/lib)

# Provide the include directory and library to the user
set(libpqxx_INCLUDE_DIR ${libpqxx_INCLUDE_DIR} CACHE PATH "Path to libpqxx include directory")
set(libpqxx_LIBRARY ${libpqxx_LIBRARY} CACHE FILEPATH "Path to libpqxx library")


