# Dhumbal Simulations

This project uses Monte Carlo simulations to analyze the card game Dhumbal.

## Project Structure

The project is organized as follows:

- `src/`: Contains the source code for the project.
  - `dhumbal.py`: Contains the logic for the Dhumbal card game.
  - `montecarlo.py`: Contains the Monte Carlo simulation logic.
  - `utils.py`: Contains utility functions used across the project.
- `notebooks/`: Contains Jupyter notebooks for data analysis and visualization.
  - `analysis.ipynb`: Notebook for data analysis and visualization.
- `tests/`: Contains unit tests for the project.
  - `test_dhumbal.py`: Contains unit tests for `dhumbal.py`.
  - `test_montecarlo.py`: Contains unit tests for `montecarlo.py`.
  - `test_utils.py`: Contains unit tests for `utils.py`.
- `.gitignore`: Specifies which files and directories Git should ignore.
- `requirements.txt`: Lists the Python packages that the project depends on.

## Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the Monte Carlo simulations, navigate to the `src/` directory and run the following command:

```bash
python montecarlo.py
```

To analyze the results, open the `analysis.ipynb` notebook in Jupyter.

## Testing

To run the unit tests, navigate to the `tests/` directory and run the following command:

```bash
python -m unittest
```

## Contributing

Contributions are welcome. Please submit a pull request with your changes.

## License

This project is licensed under the MIT License.