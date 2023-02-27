cmake_minimum_required(VERSION 3.12)
project(Hello LANGUAGES CXX)

# Add local project module path so CMake includes custom CMake modules.
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/Modules")

include(CTest)
enable_testing()

add_library(circlist
	src/CircularList.h
	src/CircularList.cpp
)
target_include_directories(circlist
	PUBLIC
		src
)
target_compile_options(circlist
	PRIVATE
		$<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:
			-Werror -Wall -Wextra>
		$<$<CXX_COMPILER_ID:MSVC>:
			/W4>
)


#
# Create executable that uses the circlist lib to process plaintext CircularList commands from the standard input.
#
add_executable(circlist_main
	src/CircularListMain.cpp
)
target_link_libraries(circlist_main
	PRIVATE
		circlist
)
target_compile_options(circlist_main
	PRIVATE
		$<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:
			-Werror -Wall -Wextra>
		$<$<CXX_COMPILER_ID:MSVC>:
			/W4>
)



#
# Create a library target for the Catch header-only test framework.
#
add_library(Catch INTERFACE)
target_include_directories(Catch
	INTERFACE
		test/
)

#
# Create a target for executing the Catch unit tests.
#
add_executable(circlist_tests
	test/main.cpp
	test/test_CircularList.cpp
)
target_include_directories(circlist_tests
	PUBLIC
		test/
)
target_link_libraries(circlist_tests
	Catch
	circlist
)
target_compile_options(circlist_tests
	PRIVATE
		$<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:AppleClang>,$<CXX_COMPILER_ID:GNU>>:
			-Werror -Wall -Wextra>
		$<$<CXX_COMPILER_ID:MSVC>:
			/W4>
)

# Load and use the .cmake file provided by Catch so all the test cases
# are made available to CTest.
include(ParseAndAddCatchTests)
ParseAndAddCatchTests(circlist_tests)

install(
	TARGETS circlist_tests
	RUNTIME DESTINATION bin
)

