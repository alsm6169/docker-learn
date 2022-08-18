## What we learned in previous chapter
- create custom container using docker file with python code within the container i.e. will be shipped with 
the container
- save output of code run from container on to a local folder

### Docker command to build the image
Refer to previous chapter for basic docker commands, additional commands  
1. build docker image from Dockerfile
`$ docker build -t docker003 .`
2. build docker image from Dockerfile with a specific tag
`$ docker build -t docker003:v2 .`
3. force rebuild of an image
`$ docker build --no-cache -t docker003 .`

## Current Chapter Scope
This is the first version of the python application to fetch the close price of the stock ticker and either display
on screen or write to a file.  
The app/eod_price.py fetches the open, high, low, close.. of the input ticker from start_date to end_date

### run docker default
```
$ docker run -it --rm docker003
os.getcwd: /app_base/app
__main__ ticker: TSLA, args.begin_date: 5, args.end_date: None, quandl: False, yahoo: True, args.file: None
fetch_price ticker: TSLA, start_date: 2022-08-13, end_date: 2022-08-18, data_src: yahoo, file_name: None
           ticker        High         Low        Open       Close    Volume  \
Date                                                                          
2022-08-15   TSLA  939.400024  903.690002  905.359985  927.960022  29786400   
2022-08-16   TSLA  944.000000  908.650024  935.000000  919.690002  29378800   
2022-08-17   TSLA  928.969971  900.099976  910.190002  911.989990  22846200   
2022-08-18   TSLA  919.500000  905.559998  918.000000  914.577087  11640629   

             Adj Close  
Date                    
2022-08-15  927.960022  
2022-08-16  919.690002  
2022-08-17  911.989990  
2022-08-18  914.577087  
```

**NOTE: -w /app_base/app is option as WORKDIR has been set in Dockerfile but if not set, it would be needed for run**  
`$ docker run -it --rm -w /app_base/app docker003`

### run docker input parameter (-it is for interactive, since we run and exit the program it is not needed)
1. specify only ticker
```
$ docker run --rm docker003 python eod_price.py AMZN
os.getcwd: /app_base/app
__main__ ticker: AMZN, args.begin_date: None, args.end_date: None, quandl: False, yahoo: True, args.file: None
fetch_price ticker: AMZN, start_date: 2022-08-17, end_date: 2022-08-18, data_src: yahoo, file_name: None
           ticker        High         Low        Open       Close    Volume  \
Date                                                                          
2022-08-17   AMZN  143.380005  140.779999  142.690002  142.100006  48070300   
2022-08-18   AMZN  142.770004  140.389893  141.320007  142.590103  22764189   

             Adj Close  
Date                    
2022-08-17  142.100006  
2022-08-18  142.590103  
```
2. specify ticker and number of day in past from today
```
$ docker run --rm docker003 python eod_price.py ACN -b 6
os.getcwd: /app_base/app
__main__ ticker: ACN, args.begin_date: 6, args.end_date: None, quandl: False, yahoo: True, args.file: None
fetch_price ticker: ACN, start_date: 2022-08-12, end_date: 2022-08-18, data_src: yahoo, file_name: None
           ticker        High         Low        Open       Close   Volume  \
Date                                                                         
2022-08-12    ACN  320.940002  314.440002  316.760010  320.440002  1774400   
2022-08-15    ACN  320.959991  317.589996  317.679993  320.329987  1125300   
2022-08-16    ACN  322.880005  318.119995  318.190002  320.779999  1596000   
2022-08-17    ACN  320.329987  315.630005  317.420013  318.450012  1505900   
2022-08-18    ACN  320.010010  316.450012  319.000000  319.269989   607472   

             Adj Close  
Date                    
2022-08-12  320.440002  
2022-08-15  320.329987  
2022-08-16  320.779999  
2022-08-17  318.450012  
2022-08-18  319.269989  
```
3. save output in file out.csv but it will not be accessible as volume is not mounted
```
$ docker run --rm docker003 python eod_price.py MSCI -f out.csv -b 8
os.getcwd: /app_base/app
__main__ ticker: MSCI, args.begin_date: 8, args.end_date: None, quandl: False, yahoo: True, args.file: out.csv
fetch_price ticker: MSCI, start_date: 2022-08-10, end_date: 2022-08-18, data_src: yahoo, file_name: out.csv
           ticker        High         Low        Open       Close    Volume  \
Date                                                                          
2022-08-10   MSCI  513.979980  503.890015  510.500000  512.119995  277200.0   
2022-08-11   MSCI  516.929993  500.380005  516.929993  501.119995  235700.0   
2022-08-12   MSCI  507.290009  499.100006  505.450012  506.709991  330900.0   
2022-08-15   MSCI  510.260010  502.440002  505.000000  508.630005  369000.0   
2022-08-16   MSCI  506.209991  495.869995  502.089996  503.619995  229900.0   
2022-08-17   MSCI  504.910004  493.359985  497.799988  502.489990  295300.0   
2022-08-18   MSCI  501.980011  499.000000  501.989990  500.869995   47668.0   

             Adj Close  
Date                    
2022-08-10  510.869995  
2022-08-11  501.119995  
2022-08-12  506.709991  
2022-08-15  508.630005  
2022-08-16  503.619995  
2022-08-17  502.489990  
2022-08-18  500.869995  

$ cat out.csv
# cat: out.csv: No such file or directory
```

4. save output in file out.csv saved in $PWD folder
```
$ docker run --rm -v "$PWD":/app_base/output -w /app_base/app docker003 python eod_price.py GOOG -f out.csv -b 3

os.getcwd: /app_base/app
__main__ ticker: GOOG, args.begin_date: 3, args.end_date: None, quandl: False, yahoo: True, args.file: out.csv
fetch_price ticker: GOOG, start_date: 2022-08-15, end_date: 2022-08-18, data_src: yahoo, file_name: out.csv
           ticker        High         Low        Open       Close    Volume  \
Date                                                                          
2022-08-15   GOOG  123.260002  121.570000  122.209999  122.879997  15525000   
2022-08-16   GOOG  123.227997  121.535004  122.320000  122.510002  15626200   
2022-08-17   GOOG  122.150002  120.199997  120.930000  120.320000  17562400   
2022-08-18   GOOG  121.639999  119.559998  120.230003  121.250000   8097958   

             Adj Close  
Date                    
2022-08-15  122.879997  
2022-08-16  122.510002  
2022-08-17  120.320000  
2022-08-18  121.250000  
$ cat out.csv 
Date,ticker,High,Low,Open,Close,Volume,Adj Close
2022-08-15,GOOG,123.26000213623047,121.56999969482422,122.20999908447266,122.87999725341797,15525000,122.87999725341797
2022-08-16,GOOG,123.22799682617188,121.53500366210938,122.31999969482422,122.51000213623047,15626200,122.51000213623047
2022-08-17,GOOG,122.1500015258789,120.19999694824219,120.93000030517578,120.31999969482422,17562400,120.31999969482422
2022-08-18,GOOG,121.63999938964844,119.55999755859375,120.2300033569336,121.25,8097958,121.25
```
## Summary
What happened here is:
we have a containerized program that fetches end of day stock price and shows the results on console 
or write it to a file