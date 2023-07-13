# PySpark Unit Testing Template

This repository provides a template for writing PySpark unit tests using `pytest` and `pyspark`. 

## Requirements

- Docker
- Visual Studio Code
- Visual Studio Code Remote - Containers Extension

## Getting Started

1. Clone this repository.
2. Open the repository in Visual Studio Code.
3. Press <kbd>F1</kbd> and select **Remote-Containers: Reopen in Container**.
4. Wait for the dev container to be built.
5. Run `pytest` to run the tests.

## How it Works

This template uses Docker and Visual Studio Code Remote - Containers Extension to create a development environment where you can run your PySpark tests.

When you open this repository in Visual Studio Code and reopen it in the dev container, the container is created and the necessary dependencies are installed. The `docker-compose.yml` file describes the configuration of the dev container. By default, it uses the `amazon/aws-glue-libs:glue_libs_4.0.0_image_01` Docker image.

When you run `pytest`, it runs the tests in the dev container. The tests use `moto` to simulate an AWS environment and a local Spark session during the tests.

## Example Test

```python
from mymodule import MyModule

def test_mymodule():
    my_module = MyModule()
    assert my_module.get_sum(1, 2) == 3
```

## Coverage

In the `pytest.ini` configuration, the `--cov` option of pytest's `addopts` is used to specify the path to the source code that needs to be covered by the tests. When running the test suite, pytest collects coverage data by tracing the execution of the code and generates a report of the code coverage.

The `--cov-config` option is used to specify a configuration file for coverage. In this case, the file setup.cfg is used to configure coverage options.

The `--cov-report` option is used to specify the format of the coverage report. In this configuration, the coverage report is generated in both HTML and terminal formats.

The `--cov option` along with the `--cov-report` option helps to measure the test coverage of the codebase. Test coverage is the measurement of how much code is exercised by the tests. This helps developers to identify untested areas of the codebase and ensure that all critical parts of the code are tested.

## Delta Lake
https://docs.delta.io/2.1.0/quick-start.html

## Style Guide
https://github.com/MrPowers/spark-style-guide/blob/main/PYSPARK_STYLE_GUIDE.md
