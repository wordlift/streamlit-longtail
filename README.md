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
$ python3.7 -m venv ~/.streamlit_ve
$ source ~/.streamlit_ve/bin/activate
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


## Main Files: Project Structure
  ```sh
  .
  ├── README.md
  ├── app.py
  ├── apps
  │   ├── spacyapi.py
  │   └── wordliftapi.py
  ├── functions
  │   ├── download.py
  │   └── interface.py
  ├── img
  │   ├── fav-ico.png
  │   ├── logo-wordlift.png
  │   └── pattern.png
  ├── multiapp.py
  ├── requirements.txt
  └── style.css 
  ```
