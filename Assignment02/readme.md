# Widget Consumer Documentation

## How to Use:

1. Install dependancies (below)
1. Navigate to src directory of this project in a cmd terminal
1. Run `python consumer.py --help` to see usage syntax

## Usage Syntax:

### Base Command:
python consumer.py

### Arguments:
--rb STRING -> ID of Bucket in Which Requests are Stored
--wb STRING -> ID of Bucket to Upload Widgets To (Incompatible with --wt)
--wt STRING -> ID of DynamoDB Table to Upload Widgets To (Incompatible with --wb)
-v FLAG -> Verbose Mode (Prints Info Messages)
--path STRING -> Path to Log File

## Dependancies

#### Python version 3.10 or Greater
```
https://www.python.org/downloads/
```

#### Boto3 Python Module
```
pip install boto3
```

#### Click Python Module
```
pip install click
```


