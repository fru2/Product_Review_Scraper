![Untitled-2025-01-19-1949](https://github.com/user-attachments/assets/187b9a4e-1cb7-4fca-a3f4-d7756ade1a7b)

## API
- https://ecgzhmjm9e.execute-api.ap-south-1.amazonaws.com/dev/api/reviews?page={url}

Basic Work
flow

1. *Input and Initial Processing:* An API accepts the page URL, and the HTML content is processed to eliminate unnecessary tags and elements. This step leverages *AWS Lambda* for efficient serverless execution.
2. *Review Section Identification:* The refined HTML is passed to an *LLM (Gemini 1.5 Flash)*, which intelligently detects the class name associated with the reviews section.
3. *Browser Automation with Playwright:* Due to *Chromium* compatibility limitations in AWS Lambda, an *AWS EC2 instance* is utilized to run *Playwright* scripts. These scripts handle browser automation tasks like navigating pages and interacting with website elements.
4. *UUID and Task Execution:* A UUID is generated on the EC2 instance to manage tasks. Using the uuid.json configuration, multiple tasks for extracting reviews are executed in parallel.
5. *Data Storage:* The collected reviews are saved to an *AWS S3 bucket*, ensuring secure and scalable storage.
6. *Data Retrieval:* Stored reviews can be accessed from the S3 bucket via on-demand requests.

### Components:

- *HTML Content Filtering:* The process begins by accepting a webpage URL, filtering its source code using tools like Beautiful Soup to extract meaningful content while discarding irrelevant elements.
- *Launching EC2 for Browser Automation:* The filtered data is sent to an EC2 instance configured to execute Playwright scripts. This setup ensures tasks like multi-page navigation and pagination handling are completed efficiently.
- *Storing JSON Data:* Extracted content from each page is processed into JSON files and uploaded to an S3 bucket for structured and scalable data storage.
- *Review Extraction via Lambda:* UUIDs corresponding to the stored JSON files are used to trigger parallel Lambda functions. These functions extract reviews from the raw source code and store the output in another S3 bucket.
