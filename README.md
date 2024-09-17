# :earth_americas: GDP dashboard template

# Date Range Generator from DataFrame

This Python script allows you to generate a date range from the last available timestamp in a given DataFrame to the current time in the UK, rounded to the nearest half-hour. It works directly on an existing DataFrame that contains timestamp data.

## Features

- Extracts the last available timestamp from a specified column in a DataFrame.
- Gets the current time in the UK and rounds it to the nearest half-hour.
- Generates a list of dates starting from the last timestamp in the DataFrame up to the current UK time.

## Requirements

- Python 3.6+
- Required libraries:
  - `pandas`
  - `pytz`

You can install the required libraries using pip:

```bash
pip install pandas pytz
