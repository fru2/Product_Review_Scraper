## Demo
Live website: https://serene-kitten-5a66fb.netlify.app/

https://github.com/user-attachments/assets/94e735fe-738e-42c1-89b4-a41e1063a14c

---
## API Endpoints
- https://ecgzhmjm9e.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?page={product_url}
```
{
    "executionArn": "",
    "status": "",
    "url": ""
}
```
Because of the bottleneck induced by the **LLM API (Gemini-1.5-flash) & Playwright**, the pipeline takes about a minute to process the data and the API timeout is 29 seconds (default) that is why I need to expose another API through which the system can poll data at a later time. 
Here `executionArn` is the system generated id to track the running process on AWS, `url` is the path to poll from the 2nd API gateway with executionArn as it's query search parameter. 
- https://o2crc9xy03.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?executionArn={your_execution_arn}
```
{
    "statusCode": ,
    "reviews_count": ,
    "reviews": [
        {
            "title": "",
            "body": "",
            "author": "",
            "rating": ""
        },
        ...
    ]
}
```
---
## Workflow
![Untitled-2025-01-19-1949](https://github.com/user-attachments/assets/187b9a4e-1cb7-4fca-a3f4-d7756ade1a7b)
#### Technologies used: 
AWS Lambda, EC2, API Gateway, and S3. The reasons for using these technologies and the challenges associated with them are discussed in a later section.
#### Components:
- *HTML Content Filtering:* The process begins by accepting a webpage URL, filtering its source code using Beautiful Soup to extract meaningful content while discarding irrelevant elements to reduce the token size before passing it on to the LLM.
- *Extract class selector:* To automate actions like pagination, extracing reviews, we need the class selector to interact with the page elements programmatically. 
- *Browser Automation:* An EC2 instance (Windows 2022 Server) runs Playwright scripts with Chromium for browser automation, as Lambda cannot handle Chromium directly.
- *Storing JSON Data:* Extracted page source code is processed into JSON files and uploaded to an S3 bucket for scalable storage. Since Step Functions have a 1MB payload limit, S3 is used to store larger JSON files, which can be several MBs.
- *Review Extraction:* Lambda uses BeautifulSoup to iterate over the JSON data in S3 and extract reviews, using dynamically fetched CSS selectors by the LLM. 
---
#### Folder structure:
```
src/
├── ec2-script/
│   └── pagination-automation/
│       └── automation.py
├── lambda-function/
│   ├── extract-css-selector/
│   │   └── lambda_function.py
│   ├── extract-reviews/
│   │   └── lambda_function.py
│   ├── filter-source/
│   │   └── lambda_function.py
│   ├── pagination-automation-trigger/
│   │   └── lambda_function.py
│   ├── poll-step-function-result/
│   │   └── lambda_function.py
│   └── trigger-step-function/
│       └── lambda_function.py
├── step-function/
│   └── MyStateMachine-t75g9b6k2.asl.json
├── test/
│   ├── filter_source_extract_class.ipynb
│   └── review_scrape_automation.ipynb
└── README.md
```
- `src/`: This folder contains all the scripts deployed on AWS. It includes Lambda functions, Step Function definitions, and EC2 scripts for automation tasks.
- `test/`: This folder contains Jupyter Notebook (.ipynb) files, which were used to create the Lambda functions and test their output during development.
---
## Challenges
- *LLM API response time:* If I prioritize performance, I will lose accuracy (e.g., getting "John Doe" instead of actual value). On the other hand, if I choose models with a larger number of parameters, the response time will be significantly slower (5–10 seconds per request).
    While selecting a model, I also need to consider RPM (Requests Per Minute) because free-tier models are generally capped at 10–15 RPM. As a result, I cannot rely heavily on LLM for review extraction.
After extensive testing and considering the trade-offs between performance and accuracy, I decided to use Gemini-1.5-flash.

- *Executing automation script on the cloud:* Ensuring seamless execution required managing resource limitations, configuring the environment, handling dependencies, and troubleshooting in a distributed setup.

#### Upcoming features
* Streaming data chunks: Because waiting 1 minute for an API call is the worst.
* Faster processing with parallel AWS task execution
* Enhanced reliability with an improved LLM
