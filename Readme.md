# paperlesspaper_client

Python client for the Paperlesspaper API

---

### Table of Contents

1. [About](#about)
2. [Installation](#installation)
   1. [With pip (recommend)](#with-pip-recommend)
   2. [From source](#from-source)
3. [Usage](#usage)
4. [Third party notices](#third-party-notices)
5. [Development](#development)
   1. [Setup environment](#setup-environment)
   2. [Tests](#tests)
   3. [Documentation](#documentation)
6. [License](#license)

### About

*paperlesspaper_client* is a python and cli client for the Paperlesspaper API. It supports the v1 of the API. You can
find the official documentation of the Paperlesspaper API [here](https://docs.paperlesspaper.de/api-guide/getting-started).

### Installation

#### With pip (recommend)

Use the following command to install *paperlesspaper_client* with pip:

```commandline
pip3 install paperlesspaper_client
```

You can also very easily update to a newer version:

```commandline
pip3 install paperlesspaper_client -U
```

#### From source

If you want to install the client from source, you can clone the repository and install it with pip:

```commandline
git clone https://github.com/infinityofspace/paperlesspaper_client.git
cd paperlesspaper_client
pip3 install .
```

### Usage

Set API token via environment variable:

```commandline
export PAPERLESSPAPER_API_KEY="your-api-token"
paperlesspaper users delete <user-id>
```

Or pass the token as an option (takes priority over environment variables):

```commandline
paperlesspaper --api-key "your-api-token" users delete <user-id>
```

Examples:

```commandline
paperlesspaper users get <user-id>
paperlesspaper users list <organization-id>
paperlesspaper devices list
paperlesspaper papers create <organization-id> <device-id> <kind>
```

Optional method arguments are passed as flags. For methods that accept dynamic payload parameters,
use `--param key=value` (repeatable).


### Third party notices

All modules used by this project are listed below:

|                         Name                          |                                              License                                              |
|:-----------------------------------------------------:|:-------------------------------------------------------------------------------------------------:|
|      [requests](https://github.com/psf/requests)      |            [Apache 2.0](https://raw.githubusercontent.com/psf/requests/master/LICENSE)            |
| [setuptools](https://github.com/pypa/setuptools)      |               [MIT](https://raw.githubusercontent.com/pypa/setuptools/main/LICENSE)               |
|    [sphinx](https://github.com/sphinx-doc/sphinx)     | [BSD 2 Clause](https://raw.githubusercontent.com/sphinx-doc/sphinx/refs/heads/master/LICENSE.rst) |
|  [responses](https://github.com/getsentry/responses)  |   [Apache 2.0](https://raw.githubusercontent.com/getsentry/responses/refs/heads/master/LICENSE)   |
|       [ruff](https://github.com/astral-sh/ruff)       |          [MIT](https://raw.githubusercontent.com/astral-sh/ruff/refs/heads/main/LICENSE)          |


_This project is not associated with Paperlesspaper or The Wire UG._

### Development

#### Setup environment

First get the source code:

```commandline
git clone https://github.com/infinityofspace/paperlesspaper_client.git
cd paperlesspaper_client
```

Now create a virtual environment, activate it and install all dependencies with the following commands:

```commandline
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Now you can start developing.

Feel free to contribute to this project by creating a pull request. Before you create a pull request, make sure that you code meets the following requirements (you can use the specified commands to check/fulfill the requirements):

 - check unit tests: `pytest`
 - format the code: `ruff format`
 - check linting errors: `ruff check`

#### Tests

Run the tests with the following command:

```commandline
pytest
```

#### Documentation

To build the documentation you can use the following commands:

```commandline
sphinx-apidoc -f -o docs/source paperlesspaper_client
cd docs && make html
```

### License

[MIT](https://github.com/infinityofspace/paperlesspaper_client/blob/master/License) - Copyright (c) Marvin Heptner
