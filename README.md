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
   pip install rc-repo-utils
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

To configure the environment variables needed for the spiritual-chatbot project, follow these steps:

1. **Update the LOG_DIR Variable**:
   
   Open the `bashrc_spiritualdata_dev` file in a text editor of your choice. Look for a line setting the `LOG_DIR` variable, and update it to a valid local filepath where logs will be stored (when using `logger.info()`). The line should look something like this:

   ```bash
   export LOG_DIR=/path/to/your/log/directory
   ```

   Replace `/path/to/your/log/directory` with the actual path where you want to store log files.

2. **Set the OPENAI_API_KEY**:

   You will also need to set your `OPENAI_API_KEY` with your personal API key. You can set this in the same `bashrc_spiritualdata_dev` file or export it separately in your shell. If you're setting it within the `bashrc_spiritualdata_dev` file, add the following line:

   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

   Replace `your-api-key-here` with your actual OpenAI API key.

   **Note**: Make sure to set your organization to Spiritual Data at [OpenAI's API keys page](https://platform.openai.com/account/api-keys) to use Spiritual Data's billing account.

3. **Source the bashrc File**:

   After editing the file, navigate to the directory containing `bashrc_spiritualdata_dev`:

   ```bash
   cd path/to/directory
   ```

   Then, source the file to apply the changes:

   ```bash
   source bashrc_spiritualdata_dev
   ```

By following these steps, you'll configure the environment variables necessary for the spiritual-chatbot project, including the log directory and OpenAI API key.

### Running the FastAPI Server

FastAPI is a web framework that allows you to create APIs quickly. Given there's a file `spiritual-chatbot/spiritualchat/api.py`, you can run the FastAPI server with the following steps:

1. Activate your virtual environment if not already activated.

2. Navigate to the directory containing `api.py`:

   ```bash
   cd spiritual-chatbot/spiritualchat
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
   cd spiritual-chatbot/spiritualchat/tests
   ```

3. Run the tests:

   ```bash
   pytest
   ```

### Conclusion

These instructions cover how to run the FastAPI server, execute tests with pytest, and set environment variables using a specific file. Always refer to the specific project documentation or consult with the development team if you encounter any specific issues or need further guidance.
