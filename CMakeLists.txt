cmake_minimum_required(VERSION 2.8.12)
project(line_profile)

set(CMAKE_CXX_STANDARD 17)

if(MSVC)
add_definitions(-DBOOST_ASIO_HAS_MOVE)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++latest")
endif(MSVC)

include_directories(${PROJECT_SOURCE_DIR}/include)

FILE(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)

find_package(pybind11 REQUIRED)


pybind11_add_module(line_profile ${SRC_FILES})