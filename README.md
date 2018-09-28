This application is written in Flask for backend, JS (D3.js) and plain html for frontend.

Version deployed on Heroku for check:

https://load-monitor-jason-heroku.herokuapp.com/

It's multi-CPU architecture and the load is very high.


To run locally, please follow these steps:

Please make sure you change your system Python version to Python3.

1. Unzip the file
2. Enter the Coding directory (the file you just unzipped)
3. Run
```
ls
```
You should be able to see files such as run.py, loadRegister.py etc

4. Assume you have installed Python3  and can use pip.

5. Install all of your requirements by running the command: 
```
pip install --upgrade -r requirements.txt
```

6. Run
```
export FLASK_APP=webserver.py
```
and then
```
flask run --host=0.0.0.0
```

7. Application should be running. Type 
```
localhost:5000 (or http://0.0.0.0:5000/)
```
in your brower to access the application.

When you open the application, it starts getting load from your system every ten seconds. The total interval is 10 minutes. And it keeps shifting the time frame.

When you hove over a certain point on the graph, you will see a window appearing notifying the time and its correspondant load value.


------------------------------------------------------------------------------------------------------------------
Run Test


In Coding directory, run the below command:
```
alias python=python3
```
then
```
python testLoadAlert.py
```

You should see all 5 tests pass.


------------------------------------------------------------------------------------------------------------------

Improvement of the app:

1. Data Storage: Currently, every data is saved in memory. When the web server shuts down or it runs for a longtime, we will either lose the data or have out of memory issue. An improvement would be to save the load data in a database, either locally or in cloud.

2. More User Interaction. Currently, user can only see load for past 10 minutes with 10s interval. We can improve the app so that user can choose various time span for example: last hour, last 6 hours etc and different intervals. Also we can make more modification to the alert messaging part so it doesn't appear in one same page. We can show the most recent 10 alerts and hide the rest and give user a button to view more.

3. Empty data points generation for D3 display. Currently, at the beginning of starting the app, it has to generate several 0 data points so the total data points number is always 60 and makes it easy for D3 to display. I am looking for a way that D3 can allocate a fixed space for each data point so even if we have only 1 data point, it will look good. But I didn't find it. And that's why write algorithm to generate empty data points. This is not a big problem, but can be improved.

4. Signature of register_load method in LoadRegister class. Currently, it takes one 'curLoad' argument. While the app is running, we actually don't pass any argument and the app will take the load from the system. The only reason why I have this argument is that we can add datapoints in test so we can control each load amount and the average over 2 minutes to check the alert logic. In real production, register_load should not have any argument and it should not allow external objects to pass any arguments. It should always take the system load and add to its own data structure.







