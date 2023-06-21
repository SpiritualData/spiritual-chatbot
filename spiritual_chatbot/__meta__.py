# `name` is the name of the package as used for `pip install package`
name = "spiritual-chatbot"
# `path` is the name of the package for `import package`
path = name.lower().replace("-", "_").replace(" ", "_")
# Your version number should follow https://python.org/dev/peps/pep-0440 and
# https://semver.org
version = "0.1.dev0"
author = "Spiritual Data"
author_email = ""
description = "Chatbot that interacts with spiritual data."  # One-liner
url = ""  # your project homepage
license = "GNU"  # See https://choosealicense.com
