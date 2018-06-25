cmake_minimum_required(VERSION 2.8.3)

project(FlexSEA-Stack-Plan)

set(SRCS
	src/flexsea_board.c
	src/flexsea_config.c
)

include_directories (
	inc

	flexsea-dephy/inc
	flexsea-dephy/DpEb42/inc
	flexsea-dephy/CycleTester/inc

	flexsea-comm/inc

	flexsea-projects/inc
	flexsea-projects/ActPack/inc
	flexsea-projects/Rigid/inc

	flexsea-system/inc
)

add_subdirectory(flexsea-comm)
add_subdirectory(flexsea-system)
add_subdirectory(flexsea-projects)
add_subdirectory(flexsea-dephy)

add_definitions(-DBUILD_SHARED_LIB_DLL -DTEST_PC -DINCLUDE_UPROJ_ACTPACK -DBOARD_TYPE_FLEXSEA_PLAN)
add_definitions(-DDEPHY)

add_library(FlexSEA-Stack-Plan_shared SHARED ${SRCS})
set_property(TARGET FlexSEA-Stack-Plan_shared PROPERTY POSITION_INDEPENDENT_CODE ON)

add_library(FlexSEA-Stack-Plan STATIC ${SRCS})
set_property(TARGET FlexSEA-Stack-Plan PROPERTY POSITION_INDEPENDENT_CODE ON)

if(WIN32)
	set(OUT_PREF "win")
else()
	set(OUT_PREF "unix")	
endif()

if(CMAKE_SIZEOF_VOID_P GREATER 4)
	set(OUT_PREF "${OUT_PREF}_64")
endif()

set_target_properties( FlexSEA-Stack-Plan_shared 
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
)

set_target_properties( FlexSEA-Stack-Plan
    PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/${OUT_PREF}"
)