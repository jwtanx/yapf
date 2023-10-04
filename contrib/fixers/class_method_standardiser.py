# Copyright 2023 @jwtanx (GitHub) All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Fixer that enforces consistent use Google style for class and function name

This script only standardise the class and method's name when they are
initialised as such

# Detected the keyword `class`
class Foo:
  ...

# Detected the keyword `def`
def bar():
  ...
"""
import re


def standardise_naming(code):
  code = _camel_case_class(code)
  code = _snake_case_method(code)
  return code


def _snake_case(code):

  def replace(match):
    name = match.group(0)

    if name == name.upper():
      return name.lower()

    for i, c in enumerate(name):
      if c.isalpha():
        alpha_index = i
        return name[:alpha_index] + "_".join(
            re.findall("[A-Z][a-z]*|[a-z]+|[0-9]+",
                       name[alpha_index:])).lower()

  # Use regex to find all valid Python identifiers (variable names) and replace them
  return re.sub(r"[a-zA-Z_][a-zA-Z0-9_]*[a-zA-Z0-9]+", replace, code)


def _camel_case_class(code):

  def replace(match):
    row = match.group(0)
    name = row.split()[1]
    parts = name.split("_")
    if len(parts) > 1:
      name_ls = [word.capitalize() for word in parts]
    else:
      name_ls = parts

    return "class " + "".join(name_ls)

  # Use regex to find all valid Python identifiers (class names) and replace them
  return re.sub(r"class \b[a-zA-Z_][a-zA-Z0-9_]*\b(\(|\:)", replace,
                code).replace("()", "")


def _snake_case_method(code):

  def replace(match):
    name = match.group(1)
    converted = _snake_case(name)
    return f"def {converted}("

  # Use regex to find all valid Python identifiers (class names) and replace them
  return re.sub(r"def (\b[a-zA-Z_][a-zA-Z0-9_]*\b)\(", replace, code)
