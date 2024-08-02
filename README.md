# TimEx: An Integrated Approach for Optimizing Time Series Visual Exploration
# Overview
TimEx is a comprehensive toolkit designed to enhance the visual exploration of time series data. It focuses on both the efficiency and effectiveness of visualizations, providing a robust framework for analyzing and interpreting complex datasets.

# Files and Descriptions
The repository contains six key files, categorized into two main purposes: efficiency and effectiveness.

# Efficiency Files
These four files evaluate the efficiency in terms of the number of operations:

TimEx_Subsequence_Length(R): Varies the subsequence length while keeping the shift length and k value constant.
TimEx_Shift_Length(R): Varies the shift length while keeping the subsequence length and k value constant.
TimEx_K: Varies the k values while keeping the subsequence and shift lengths constant.
TimEx_Splitting: Splits the data into three segments to monitor behavior under different data characteristics.

# Effectiveness Files
One file assesses the effectiveness based on the quality of the recommended visualizations:

Effectiveness_Subsequence_Length(R)_K: Varies the subsequence length, k value and shift length.

# CSV files
There are 5 csv files for 5 countries; United Arab Emirates (AE.csv), United State (US.csv), Brazil (BR.cvs), Korea (KR.csv) and Australlia (AU.csv).
Each python file is executed seperately for each CSV file and then take the average of the result.

# Usage
To use TimEx, you will need Python installed on your system. Each file can be executed independently to analyze different aspects of the time series data. Detailed instructions and examples are provided within each script.
     
