### **Sales Analytics System**



1. ##### Project Structure-



Replicate the below folder structure in your local machine after downloading the files from - 

"https://github.com/muditrajkaith/sales-analytics-system"

 



sales-analytics-system/

│

├── data/

│   └── sales\_data.txt

│

├── output/

│   └── sales\_report.txt

│

├── utils/

│   ├── file\_handler.py

│   ├── data\_processor.py

│   ├── api\_handler.py

│   └── report\_generator.py

│

├── main.py

├── requirements.txt

└── README.md







#### 2\. Setup and Run Instructions-



Prerequisites-



* Python 3.9 or above installed
* Internet connection (for API integration)





###### Step 1: Install dependencies



Create a virtual environment (recommended):

python -m venv venv





Activate it:



Windows-

venv\\Scripts\\activate





Mac/Linux-

source venv/bin/activate





Install required packages:

pip install -r requirements.txt





###### Step 2: Verify input file



Ensure the sales data file exists at:

data/sales\_data.txt





###### Step 3: Run the application



Execute the main program:

python main.py





###### Step 4: Output files



After successful execution, the following files will be generated:

data/enriched\_sales\_data.txt

output/sales\_report.txt



