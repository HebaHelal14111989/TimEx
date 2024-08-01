TimEx: An Integrated Approach for Optimizing Time Series Visual Exploration
Overview
TimEx is a comprehensive toolkit designed to enhance the visual exploration of time series data. It focuses on both the efficiency and effectiveness of visualizations, providing a robust framework for analyzing and interpreting complex datasets.

Files and Descriptions
The repository contains six key files, categorized into two main purposes: efficiency and effectiveness.

Efficiency Files
These four files evaluate the efficiency in terms of the number of operations:

TimEx_Subsequence_Length(R): Varies the subsequence length while keeping the shift length and k value constant.
TimEx_Shift_Length(R): Varies the shift length while keeping the subsequence length and k value constant.
TimEx_K: Varies the k values while keeping the subsequence and shift lengths constant.
TimEx_Splitting: Splits the data into three segments to monitor behavior under different data characteristics.
Effectiveness Files
These two files assess the effectiveness based on the quality of the recommended visualizations:

Effectiveness_Subsequence_Length(S)_K: Varies the shift length and k value while keeping the subsequence length constant.
Effectiveness_Subsequence_Length(R)_K: Varies the subsequence length and k value while keeping the shift length constant.
Usage
To use TimEx, you will need Python installed on your system. Each file can be executed independently to analyze different aspects of the time series data. Detailed instructions and examples are provided within each script.
     
