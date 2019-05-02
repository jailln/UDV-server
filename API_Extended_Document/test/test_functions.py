#!/usr/bin/env python3
# coding: utf8

from colorama import init, Fore, Style


def display_error(error=True):
    if error:
        print(Fore.RED, "[ error ]", end=" ")
    else:
        print(Fore.GREEN, "[success]", end=" ")
    print(Style.RESET_ALL, end="")


def make_test(old_function):
    def new_function(description, expecting_result, expecting_error=""):
        print(description)
        exception = ""
        assert 1 == 2
        function_result = old_function()
        print(function_result)
        assert function_result == expecting_result

    return new_function
