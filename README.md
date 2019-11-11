# FHMP
oTree-based experiment

## Testing

### in local environment
Please refer to the [Wiki](https://github.com/mendoza-research/fhmp/wiki) for instructions on setting up a local testing environment. 

### in Heroku
To test on a server environment, please setup a Heroku project using [oTree Hub](https://www.otreehub.com/). 

### Setting number of participants for split window testing
It is easier to test using the split window feature offered by oTree.<br />
Currently, the maximum number of players supported by split window is 3.<br />
To test locally using split windows, set the `num_demo_participants` to 3 in `settings.py`.

![image](https://user-images.githubusercontent.com/1064036/68621295-b3a97980-0512-11ea-8da7-226a3004f121.png)

### Setting environment variables to test different treatments

In `treatments.py`, uncomment the lines below, and set the values to either `'True'` or `'False'` (note that they should be string values, not boolean since environment variables can only be strings).  

```python
# For local testing
os.environ['CAN_CHOOSE_PRECISION'] = 'False'
os.environ['IS_GRADE_PASS_FAIL'] = 'True'
```


## Setting treatment environment variables in Heroku
- For just the `No-Choice-Grades` and `No-Choice-Pass-Fail` conditions, there should be no SellerChoiceHighLow page shown, as they are not given the choice. All Sellers are forced to see the more precise options.
- For just the `No-Choice-Grades` and `Choice-Grades` conditions, fact checker grade will return Pass/Fail instead of A,B,C and F. 

To set these variables, please go to "Settings" in Heroku project page.<br /><br />
![image](https://user-images.githubusercontent.com/1064036/68620852-b5bf0880-0511-11ea-8e3c-864c0b44cdb1.png)

Scroll down to **Config Vars**.<br /><br />
![image](https://user-images.githubusercontent.com/1064036/68620940-ebfc8800-0511-11ea-8f34-3df8a9cc9ac2.png)

Add two variables `CAN_CHOOSE_PRECISION` and `IS_GRADE_PASS_FAIL`. The values should be either `True` or `False`.<br /><br />
![image](https://user-images.githubusercontent.com/1064036/68621082-3847c800-0512-11ea-8f45-ae0c4d48b0b5.png)
