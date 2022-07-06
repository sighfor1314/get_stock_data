## Description
###  description
    get_all_stock_number.py : Get all stock_code,stock_name,industry_type
    stock_info.py : Get all stock info from twse API and generate dairly json
    top3_industry.py : Calculate top3 ChangeRate of industry  

### Deploy to AWS lambda
    1. Create function and select python3.9
    2. Create a deployment package with the installed library 
    3. Generate a .zip file
    4. Add .zip to layer
### AWS CloudWatch Events 
    1. Set cron from Amazon EventBridge 
    2. Select AWS service >> Lambda >> function
    3. Created
    
### Testing
    1. Check response status is '200'
    2. Check response is not {} (empty)
    3. Check from API date is today or not update
    4. Check industry_type count is correct
    5. Check listed.json is existed
    6. Check {industry}_top3.json is al existed
### Notes
    2022xxxx_listed only for testing
