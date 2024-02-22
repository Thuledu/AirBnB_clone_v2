#!/usr/bin/python3
""" Unit tests for console (command interpreter)."""
import MySQLdb
import json
import unittest
import os
import sqlalchemy
from unittest.mock import patch
from io import StringIO

class TestCreateObject(unittest.TestCase):
    def setUp(self):
        self.console = Console()

    def test_create_with_string_param(self):
        command = "create MyClass name=\"My_little_house\""
        expected_output = "76b65327-9e94-4632-b688-aaa22ab8a124"
        self.assertEqual(self.console.do_create(command), expected_output)

    def test_create_with_float_param(self):
        command = "create MyClass float_param=3.14"
        expected_output = "some_expected_output"
        self.assertEqual(self.console.do_create(command), expected_output)

    def test_create_with_invalid_param(self):
        command = "create MyClass invalid_param=abc"
        expected_output = "some_expected_output"
        self.assertEqual(self.console.do_create(command), expected_output)
