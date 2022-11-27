# My task

## Setup
Clone the repo and move into it:
```sh
git clone https://github.com/gavjan/my_task && cd my_task
```

Install python dependencies:
```sh
pip3 install requirements.txt
```
## CLI Version
Run CLI version with:
```sh
python3 src/main.py
```

## GUI Version
Run GUI version with:
```sh
python3 src/main.py
```
It is also possible to compile the GUI version into an executable with `pyinstaller`

Install pyinstaller(if pip fails to install pyinstaller please refer to the [pyinstaller installation guide](https://pyinstaller.org/en/stable/installation.html)):
```sh
pip3 install pyinstaller
```

Compile the GUI:
```sh
mkdir build && cd build
pyinstaller --onefile --noconsole ../src/gui.py
```
on success, the compiled binary will be under `build/dist/gui`

Notes:
- On MacOS the executable will be `build/dist/gui.app`
- On Windows the executable will be `build/dist/gui.exe`
- Executables compiled with pyinstaller are designed for machines with the same Operating System as the one used to compile the binary, so for example a binary compiled with Linux can only run on Linux machines and not MacOS or Windows.



## Test
Tests are located in `test/tests`, where each folder is a test; inside `response.json` is the mocked response that the test should send to the application, and `answer.json` is the asnwer it expects from the application.

To run the tests:
```sh
cd test && python3 mock_test.py
```




