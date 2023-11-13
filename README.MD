# **Rwanda Economic Dashboard: An Interactive Visualization of GDP and CPI Trends**

This interactive dashboard presents economic data for Rwanda, utilizing the Python framework Streamlit. The dashboard incorporates two key datasets: GDP and CPI data from the National Institute of Statistics of Rwanda (NISR) and CPI data from the National Bank of Rwanda (BNR).

## Data Sources

* GDP data: National Institute of Statistics of Rwanda (NISR): https://www.statistics.gov.rw/publication/1914
* CPI data: National Institute of Statistics of Rwanda (NISR): https://www.statistics.gov.rw/publication/1873

## Features

* Visualizes trends in GDP and CPI over time
* Allows users to explore and analyze data interactively
* Provides insights into the economic performance of Rwanda

## Technology Stack

* Streamlit: Python framework for creating interactive data visualizations
* Pandas: Python library for data manipulation and analysis
* Matplotlib: Python library for data visualization

## Usage

1. Clone the repository
2. Install Streamlit:
   ```
   pip install streamlit
   ```
3. install all project dependices:
   ```
   pip install -r requirements.txt
   ```
4. Run the dashboard:
   ```
   streamlit run app.py
   ```

## License

**MIT License**

## Running this Projects with Pip Virtual Environments and Pip Requirements

Streamlit projects are typically run using a Pip and virtual environment to isolate the project's dependencies from the global Python environment. This ensures that the project's dependencies do not interfere with other projects or the system Python environment.

### Installing Pip and venv

To manage virtual environments and install Pip requirements, you'll need to install Pip

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
