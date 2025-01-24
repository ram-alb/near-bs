# Near BS

This Python tool automates the process of configuring 4G LTE base stations to act as anchors for 5G base stations in non-standalone (NSA) 5G networks. NSA 5G requires 4G stations to handle control signaling, while 5G manages data traffic. The tool efficiently finds the nearest 5G station for each 4G station, ensuring there are no other 4G stations in between, and configures the necessary parameters on the 4G stations to support NSA 5G connectivity.

## Requirements

To use this project, ensure you have the following installed:
- [Poetry](https://python-poetry.org/): Python dependency management and packaging tool.
- [Make](https://www.gnu.org/software/make/manual/html_node/index.html): GNU make utility.
- Create a `local_lib` directory in the root of your project and place the `enm_client_scripting-1.22.2-py2.py3-none-any.whl` file inside it.
- .env file with next variables
ATOLL_HOST
ATOLL_PORT
SERVICE_NAME
ATOLL_LOGIN
ATOLL_PASSWORD
ENM_2_IP
ENM_2
ENM_4
ENM_LOGIN
ENM_PASSWORD
ENM_PORT
EMAIL_ADDRESS
EMAIL_HOST
TO

## Installation
- clone the repository:
```bash
git clone
```

- add .env file to the root of the project
- add local_lib directory with enmscripting library to the root
- install dependencies:
```bash
make install
```

## Usage
- To get csv file with LTE-NR pairs run:
```bash
poetry run get-csv
```
csv file will be generated in the root of the project

- To run mobatch for NR anchor configuration run:
```bash
poetry run mobatch
```


# Near BS

This Python tool automates the process of configuring 4G LTE base stations to act as anchors for 5G base stations in non-standalone (NSA) 5G networks. NSA 5G requires 4G stations to handle control signaling, while 5G manages data traffic. The tool efficiently finds the nearest 5G station for each 4G station, ensuring there are no other 4G stations in between, and configures the necessary parameters on the 4G stations to support NSA 5G connectivity.

## Requirements

To use this project, ensure you have the following installed:

- [Poetry](https://python-poetry.org/): Python dependency management and packaging tool.
- [Make](https://www.gnu.org/software/make/manual/html_node/index.html): GNU make utility.
- `enm_client_scripting-1.22.2-py2.py3-none-any.whl` Library: Place this file in a local_lib directory created at the project root.
- A `.env` file with the following variables:
```dotenv
  ATOLL_HOST
  ATOLL_PORT
  SERVICE_NAME
  ATOLL_LOGIN
  ATOLL_PASSWORD
  ENM_2_IP
  ENM_2
  ENM_4
  ENM_LOGIN
  ENM_PASSWORD
  ENM_PORT
  EMAIL_ADDRESS
  EMAIL_HOST
  TO
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/ram-alb/near-bs.git
```
2. Add the .env file to the root of the project.
3. Add the local_lib directory with the `enm_client_scripting` library to the root.
4. Install dependencies:
```bash
make install
```

## Usage
- To generate a CSV file with LTE-NR pairs, run:
```bash
poetry run get-csv
```
The CSV file will be generated in the root of the project.
- To run mobatch for NR anchor configuration, run:
```bash
poetry run mobatch
```

## Notes
- Ensure that the .env file is properly configured with the necessary environment variables before running the scripts.
- The tool works by automating the configuration and pairing of 4G LTE and 5G NR stations for seamless NSA 5G connectivity.

## Contributing
Contributions are welcome! If you would like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch `git checkout -b feature/YourFeature`.
3. Commit your changes `git commit -m 'Add some feature'`.
4. Push to the branch `git push origin feature/YourFeature`.
5. Open a Pull Request.