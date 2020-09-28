cmake_minimum_required(VERSION 3.5)

project(Igrulka_Qt LANGUAGES CXX)

set(CMAKE_INCLUDE_CURRENT_DIR ON)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# QtCreator supports the following variables for Android, which are identical to qmake Android variables.
# Check http://doc.qt.io/qt-5/deployment-android.html for more information.
# They need to be set before the find_package(Qt5 ...) call.

#if(ANDROID)
#    set(ANDROID_PACKAGE_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/android")
#    if (ANDROID_ABI STREQUAL "armeabi-v7a")
#        set(ANDROID_EXTRA_LIBS
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libcrypto.so
#            ${CMAKE_CURRENT_SOURCE_DIR}/path/to/libssl.so)
#    endif()
#endif()

find_package(QT NAMES Qt6 Qt5 COMPONENTS Widgets REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} COMPONENTS Widgets REQUIRED)

if(ANDROID)
  add_library(Igrulka_Qt SHARED
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
  )
else()
  add_executable(Igrulka_Qt
    main.cpp
    mainwindow.cpp
    mainwindow.h
    mainwindow.ui
    settlement.cpp
    settlement.h
    pops.cpp
    pops.h
    generators.cpp
    game_cycle.cpp
    game_cycle.h
    culture.cpp
    culture.h
    factory.cpp
    factory.h
    goods.cpp
    goods.h
    religion.cpp
    religion.h
    state.cpp
    state.h
    strata.cpp
    strata.h
  )
endif()

target_link_libraries(Igrulka_Qt PRIVATE Qt${QT_VERSION_MAJOR}::Widgets)
