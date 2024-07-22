# SonarQube Export Issues

Export all SonarQube issues to excel file from all projects matching a wildcard pattern.

## Prerequisites

- Python 3.x
- `pandas` library
- `requests` library
- Access to a SonarQube instance with an appropriate auth token

## Installation

To install the required packages, run:
```bash
pip install -r requirements.txt
```

## Usage

To run the export script, use:
```bash
python export.py
```

## Input Parameters

- `--sonarqube_export_url` or environment variable `SONARQUBE_EXPORT_URL` (default: `http://localhost:9000`)
- `--sonarqube_export_auth_token` or environment variable `SONARQUBE_EXPORT_AUTH_TOKEN`
- `--project_pattern` wildcard pattern (default: all)

Example with auth token
```bash
python export.py --sonarqube_export_auth_token=[Token]
```


## Oputput
Excel files in format `sonarqube_issues_[project_ket]_[YYYYMMDD].xlsx`

## License

This project is licensed under the Apache 2.0 License.