## WordLift's Search Intent Inspector Streamlit App
This is the repository for the streamlit web application of the the long-tail query inspector.
A tool meant to help you find new query opportunities.


## How to Run
1. Change to your directory:
```
$ cd my/directory
```
2. Virtual environment:
```
$ python3.7 -m venv ~/.virtual_env_name
$ source ~/.virtual_env_name/bin/activate
```
3. Install dependencies:
```
$ pip install -U pip
$ pip install -r requirements.txt
```
4. Start the application:
```
$ streamlit run app.py
```


## Main Files:
  ```sh

  .
  ├── Dockerfile
  ├── Interface.py
  ├── README.md
  ├── app.py *** driver of the app
  ├── config.toml
  ├── credentials.toml
  ├── download.py
  ├── img
  │   ├── fav-ico.png
  │   ├── logo-wordlift.png
  │   └── pattern.png
  ├── requirements.txt *** The dependencies we need to install with "pip install -r requirements.txt"
  └── style.css

  ```
