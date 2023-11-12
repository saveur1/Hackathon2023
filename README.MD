# Streamlit-Dashboard-Descriptive-Analytics-with-MYSQL

What is descriptive analytics?

Descriptive analytics is a type of data analytics that looks at past data to give an account of what has happened. Results are typically presented in reports, dashboards, bar charts and other visualizations that are easily understood.

Descriptive statistics provide simple summaries about the sample and about the observations that have been made. Such summaries may be either quantitative, i.e. summary statistics, or visual, i.e. simple-to-understand graphs. These summaries may either form the basis of the initial description of the data as part of a more extensive statistical analysis, or they may be sufficient in and of themselves for a particular investigation.

## Running this Projects with Pip Virtual Environments and Pip Requirements

Streamlit projects are typically run using a Pip and virtual environment to isolate the project's dependencies from the global Python environment. This ensures that the project's dependencies do not interfere with other projects or the system Python environment.

### Installing Pip and venv

To manage virtual environments and install Pip requirements, you'll need to install Pip

Bash

```
python3 -m venv venv
```

### Creating a Virtual Environment

Once Pip is installed,  Navigate to the project directory and create a virtual environment using the following command:

Bash

```
python3 -m venv venv
```

This will create a virtual environment named `venv` within the project directory.

### Installing Pip Requirements

Activate the virtual environment using the following command:

Bash

```
source venv/bin/activate
```

Once the virtual environment is activated, install the project's Pip requirements using the following command:

Bash

```
pip install -r requirements.txt
```

This will install all of the project's dependencies specified in the `requirements.txt` file.

### Running the Streamlit Project

With the virtual environment activated and the Pip requirements installed, you can run the Streamlit project using the following command:

Bash

```
streamlit run app.py
```

This will launch the Streamlit project in your web browser.

### Closing the Pip Virtual Environment

To deactivate the virtual environment, use the following command:

Bash

```
deactivate
```

This will deactivate the virtual environment and restore your system Python environment.
