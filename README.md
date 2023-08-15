### 1. Prepare the System

Make sure you have Python installed on your system. If not, you can download and install it from the [official Python website](https://www.python.org/downloads/).

Also, ensure that you have Git installed to clone the repositories. You can download and install it from the [official Git website](https://git-scm.com/).

### 2. Create a Python Virtual Environment

A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python and some additional packages.

Here's how to create a virtual environment:

a. Open a terminal or command prompt.

b. Navigate to the directory where you want to create the virtual environment.

c. Run the following command:

   ```bash
   python3 -m venv spiritual_env
   ```

d. Activate the virtual environment:

   - **Windows**: `.\spiritual_env\Scripts\activate`
   - **Linux/Mac**: `source spiritual_env/bin/activate`

### 3. Clone and Install spiritualdata-utils

a. Clone the spiritualdata-utils repository:

   ```bash
   git clone git@github.com:SpiritualData/spiritualdata-utils.git
   ```

b. Navigate to the cloned directory:

   ```bash
   cd spiritualdata-utils
   ```

c. Install spiritualdata-utils in development mode:

   ```bash
   python setup.py develop
   ```

### 4. Clone and Install spiritual-chatbot

a. Navigate back to the main directory (or a directory of your choice):

   ```bash
   cd ..
   ```

b. Clone the spiritual-chatbot repository:

   ```bash
   git clone git@github.com:SpiritualData/spiritual-chatbot.git
   ```

c. Navigate to the cloned directory:

   ```bash
   cd spiritual-chatbot
   ```

d. Install the spiritual-chatbot in development mode using pip:

   ```bash
   pip install -e .
   ```

### Setting Environment Variables Using bashrc_spiritualdata_dev

If you have a file named `bashrc_spiritualdata_dev` that contains environment variables needed for development, you can source this file to set those variables:

1. Navigate to the directory containing `bashrc_spiritualdata_dev`:

   ```bash
   cd path/to/directory
   ```

2. Source the file:

   ```bash
   source bashrc_spiritualdata_dev
   ```

This will set the environment variables defined in the file for your current session. You may want to include this step in your startup scripts if you need these variables every time you work on the project.

### Running the FastAPI Server

FastAPI is a web framework that allows you to create APIs quickly. Given there's a file `spiritual-chatbot/spiritual_chat/api.py`, you can run the FastAPI server with the following steps:

1. Activate your virtual environment if not already activated.

2. Navigate to the directory containing `api.py`:

   ```bash
   cd spiritual-chatbot/spiritual_chat
   ```

3. Run the FastAPI server:

   ```bash
   uvicorn api:app --reload
   ```

   This command assumes that `app` is the FastAPI instance in your `api.py` file. The `--reload` flag makes the server restart upon code changes, which is useful during development.

4. You can access the API documentation at `http://127.0.0.1:8000/docs` in your web browser.

### Running Tests with pytest

To run the tests for the spiritual-chatbot project using pytest, follow these steps:

1. Make sure pytest is installed in your virtual environment. If not, install it:

   ```bash
   pip install pytest
   ```

2. Navigate to the tests directory:

   ```bash
   cd spiritual-chatbot/spiritual_chat/tests
   ```

3. Run the tests:

   ```bash
   pytest
   ```

### Conclusion

These instructions cover how to run the FastAPI server, execute tests with pytest, and set environment variables using a specific file. Always refer to the specific project documentation or consult with the development team if you encounter any specific issues or need further guidance.
