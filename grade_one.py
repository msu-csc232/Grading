#!/usr/bin/python3

import os
import subprocess
import sys

from pathlib import Path

expected_num_args = 4
assignment_arg_index = 1
assignment_num_arg_index = 2
username_arg_index = 3
command_line_syntax_error_code = 2

if len(sys.argv) == expected_num_args:
    assignment = sys.argv[assignment_arg_index]
    if len(sys.argv[assignment_num_arg_index]) == 1:
        number = "0" + sys.argv[assignment_num_arg_index]
    else:
        number = sys.argv[assignment_num_arg_index]
    username = sys.argv[username_arg_index]

    repository = assignment + number + "-" + username
    script_dir = os.getcwd()
    clone_dir = assignment + number + "-" + username

    if assignment == "hw":
        os.chdir(script_dir + "/Hw")
    elif assignment == "lab":
        os.chdir(script_dir + "/Labs")
    else:
        sys.exit(command_line_syntax_error_code)

    if os.path.isdir(clone_dir):
        rmdir_cmd = ["rm", "-rf", clone_dir]
        current_process = subprocess.run(rmdir_cmd, stdout=subprocess.PIPE, encoding="utf-8")
        print(current_process.stdout)

    # Clone the assignment
    git_clone_cmd = ["git", "clone", "git@github.com:msu-csc232/{0}.git".format(clone_dir)]
    current_process = subprocess.run(git_clone_cmd, stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)

    # Navigate into cloned directory
    os.chdir(clone_dir)

    # Check out the develop branch
    git_checkout_cmd = ["git", "checkout", "develop"]
    current_process = subprocess.run(git_checkout_cmd, stdout=subprocess.PIPE, encoding="utf-8")
    current_process_output = current_process.stdout
    print(current_process.stdout)

    # Navigate into a builder directory
    # At least two different paths have been specified in the past so we'll try either one...
    if os.path.isdir("generator/unix"):
        os.chdir("generator/unix")
    elif os.path.isdir("build/unix"):
        os.chdir("build/unix")
    else:  # None of the expected paths exist so we'll make one to use
        os.makedirs("tmp/unix")
        os.chdir("tmp/unix")

    # cmake -G "Unix Makefiles" ../..
    cmake_cmd = ["cmake", "-G", "Unix Makefiles", "../.."]
    current_process = subprocess.run(cmake_cmd, stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)

    # make
    make_cmd = ["make"]
    current_process = subprocess.run(make_cmd, stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)

    main_exe = Path("../../out/{0}{1}".format(assignment, number))
    demo_exe = Path(".")  # dummy initialization
    test_exe = Path(".")  # dummy initialization

    if main_exe.is_file():
        demo_exe = Path("../../out/{0}{1}Demo".format(assignment, number))
        test_exe = Path("../../out/{0}{1}Test".format(assignment, number))
    elif Path("../../out/{0}{1}".format("%s%s" % (assignment[0].upper(), assignment[1:]), number)).is_file():
        # Just in case the assignment was capitalized in the CMakeLists.txt file...
        assignment = "%s%s" % (assignment[0].upper(), assignment[1:])
        main_exe = Path("../../out/{0}{1}".format(assignment, number))
        demo_exe = Path("../../out/{0}{1}Demo".format(assignment, number))
        test_exe = Path("../../out/{0}{1}Test".format(assignment, number))

    # Execute the programs
    current_process = subprocess.run([main_exe], stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)
    current_process = subprocess.run([demo_exe], stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)
    current_process = subprocess.run([test_exe], stdout=subprocess.PIPE, encoding="utf-8")
    print(current_process.stdout)
    os.chdir(script_dir)
    print(os.getcwd())
else:
    print("Usage:", sys.argv[0], "assignment number username")
    print("\twhere assignment = [hw|lab],\n\tnumber = [1|2|...|12]")
    print("\tusername is the student's GitHub username...")
    sys.exit(command_line_syntax_error_code)  # Command-line syntax error
