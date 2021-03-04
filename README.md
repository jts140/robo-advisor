# robo-advisor

A program that will recommend stock picks to a user

(https://github.com/jts140/robo-advisor)

## Prerequisites

  + Anaconda 3.7+
  + Python 3.7+
  + Pip

## Installation

Clone or Download from (Github Source) (https://github.com/jts140/robo-advisor), then navigate into the project repository:

'''sh
cd robo-advisor

Use Anaconda to create and activate a new virtual environment, perhaps called "stocks-env":

```sh
conda create -n stocks-env python=3.8
conda activate stocks-env
```

From inside the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

> NOTE: if this command throws an error like "Could not open requirements file: [Errno 2] No such file or directory", make sure you are running it from the repository's root directory, where the requirements.txt file exists (see the initial `cd` step above)


## Setup
##UPDATE when program is built

In in the root directory of your local repository, create a new file called ".env", and update the contents of the ".env" file to specify the tax rate of your local area:
  '''
  ALPHAVANTAGE_API_KEY="abc123"
  '''
> NOTE: the ".env" file is usually the place for passing configuration options and secret credentials, so as a best practice we don't upload this file to version control (which is accomplished via a corresponding entry in the [.gitignore](/.gitignore) file)

## Usage

Run the program 

'''py
python robo-advisor.py
'''

> NOTE: if you see an error like "ModuleNotFoundError: No module named '...'", it's because the given package isn't installed, so run the `pip` command above to ensure that package has been installed into the virtual environment
