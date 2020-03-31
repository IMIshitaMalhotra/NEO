# Near Earth Object Database

The Near Earth Object database is a searchable Python 3 command-line interface (CLI) project.

# Install

A Python 3.6+ project, no external dependencies are required as all libraries used are a part of the Python standard library.

If you have multiple versions of Python installed on your machine, please be mindful [to set up a virtual environment with Python 3.6+](https://docs.python.org/3/library/venv.html).

## To Setup a Python 3  Virtual  Environment

```python3 -m venv /path/to/new/virtual/environment```

# Usage

To use the project:

1. Clone the project to your local machine
2. Create a virtual environment, named `env`, with `python3 -m env /env` in project root
3. Activate the virtual environment with `source env/bin/activate`
4. Run `python main.py -h` or `./main.py -h` for an explanation of how to run the project
5. Or try it out yourself!

Example of how to use the interface:

1. Find up to 10 NEOs on Jan 1, 2020 displaying output to terminal

`./main.py display -n 10 --date 2020-01-01`

2. Find up to 10 NEOs from input file 'new_neo_data.csv' between Jan 1, 2020 and Jan 10, 2020 within 5 km from Earth,
exporting to a csv file

`./main.py csvfile -n 10 -f new_neo_data.csv --start_date 2020-01-01 --end_date 2020-01-10 --filter distance:>=:5`

## Requirements

All libraies that are required are provided in the `requirements.txt` file

## Features
Search Features:

   1.  Find up to some number of unique NEOs on a given date or between start date and end date.
   2.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers.
   3.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
       that were hazardous.
   4.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
       that were hazardous and within X kilometers from Earth.


To run your implementation, you can run `main.py` which has been provided to you. Examples of how to run it are below:

```
# For running an example of Features 1: find a unique number of NEOs on a date that will be displayed to stdout

./main.py display -n 10 --date 2020-01-01

# For running an example of Features 2: find a unique number of NEOs between dates that are not hazardous. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False"

# For running an example of Features 3: find a unique number of NEOs between dates that are not hazardous, have a diameter greater than 0.02 units. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False" "diameter:>:0.02"

# For running an example of Features 4: find a unique number of NEOs between dates that are not hazardous, have a diameter greater than 0.02 units, that were more than 50000 units away. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False" "diameter:>:0.02" "distance:>=:50000"
```
## Near Earth Object Data

Each row in the `neo_data.csv` represents a single orbit path for a Near Earth Object on a given date.

<details>
 <summary> Each row includes the following attributes: </summary>

```
- id: unique id of the NEO 
- neo_reference_id: NEO reference id 
- name: NEO name 
- nasa_jpl_url: url with NASA info on the NEO 
- absolute_magnitude_h: height of NEO 
- estimated_diameter_min_kilometers: diameter in km min 
- estimated_diameter_max_kilometers: diameter in km max 
- estimated_diameter_min_meters: diameter in m min  
- estimated_diameter_max_meters: diameter in m max  
- estimated_diameter_min_miles: diameter in mi min  
- estimated_diameter_max_miles: diameter in mi max  
- estimated_diameter_min_feet: diameter in ft min  
- estimated_diameter_max_feet: diameter in ft max  
- is_potentially_hazardous_asteroid: true/false if hazaradous  
- kilometers_per_second: km pr s 
- kilometers_per_hour: km per hr 
- miles_per_hour: mi per hr 
- close_approach_date: str of NEO orbit close approach date 
- close_approach_date_full: : str of NEO orbit close approach date 
- miss_distance_astronomical: : how far NEO miss in astronomical units 
- miss_distance_lunar: how far NEO miss in lunar units  
- miss_distance_kilometers: how far NEO miss in km 
- miss_distance_miles: how far NEO miss in mi 
- orbiting_body: body orbiting around 
```

</details>

