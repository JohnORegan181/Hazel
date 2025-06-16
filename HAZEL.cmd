@echo off
chcp 65001 > nul


if /I  "%~1"=="" (
    echo Hazel CLI - missing input file or command.
    echo Usage: HAZEL file.haz.
    echo Type "HAZEL intro" for an introduction.
    exit /b
)

if /I  "%1"=="licence" (
    echo © 2025 John O' Regan
    echo Hazel is source-available. See LICENSE.md for full terms.
    exit /b
)

if /I  "%1"=="--licence" (
    echo © 2025 John O' Regan
    echo Hazel is source-available. See LICENSE.md for full terms.
    exit /b
)

if /I  "%1"=="ver" (
    echo 1.0.1
    exit /b
)

if /I  "%1"=="creator" (
    echo https://www.youtube.com/@JumperVr
    exit /b
)

if /I  "%1"=="info" (
    echo Hazel was a programming language made by John O' Regan.
    echo To see hazel's current version type "HAZEL ver".
    echo To see who created Hazel type "HAZEL creator".
    echo To see the Hazel licence type "HAZEL licence".
    echo To see the Hazel changelogs type "HAZEL changelogs"
    echo To run Hazel type "HAZA [file directory]".
    exit /b
)

if /I  "%1"=="intro" (
    echo Hazel was a programming language made by John O' Regan.
    echo Hazel is a side project and has it's genisis in a simple number calculator.
    echo Type "HAZEL info" for more information.
    exit /b
)

if /I  "%1"=="changelogs" (
    echo Hazel version 1.0.1 .
    echo changes: [
    echo - Changed .bat to files to .cmd files
    echo - Added a example Hazel program which is named Example.haz
    echo - Added exponentiation operator which is "^"
    echo - Made TOUTP turn its input into a string
    echo ]
    exit /b
)

if /I  "%1"=="--help" (
    
    echo If you need any help type "HAZEL intro"
    exit /b
)




REM Launch Hazel interpreter with file path
python HAZINT.py %1
