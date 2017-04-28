# FindLaundryInfo
### Python 3.6
### Objective
FindLaundryInfo is a script that retrieves Laundry data regarding washing and drying machines being used (how many laundry machines are open). This is all done through the UMass Laundry Tracker.
### Why?
This script is written in part of a data analysis project that looks at washing, and drying machine usage data and analyze the habits of college students across campus. UMass Laundry Tracker has information on all laundry rooms and their respective washing and drying machines. By using this information and retrieving it in a timely fashion, we can construct a data model that predicts habits of different dormitories across the UMass campus. 
With enough information, we can predict:
* Broken Laundry Machines
* Population
* Events correlated with Laundry

### Sample Output
```
------------------------------------
   Res.Hall        Washer   Dryer
------------------------------------
   North_A            5       7
   Butterfield        4       1
   Webster            5       5
                .
                .
                .
   Pierpont           4       4
   Melville           3       3
   Prince             2       2
```

### Required Libraries
* Selenium
