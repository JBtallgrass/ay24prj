# ay24prj

### Explanation:

1. **Reading Data:**
- Each CSV file is read and a unique identifier `unique_id` is created by concatenating the first letter of the last name, the first letter of the first name, and the learner ID.

2. **Combining Data:**
- All data is concatenated into a single DataFrame, ensuring each student's performance across all blocks is included.

3. **Data Inspection:**
- Print some basic information about the combined DataFrame.

4. **Data Cleaning:**
- Handle missing values and ensure correct data types.

5. **Helper Columns:**
- Create a `team_section` column.

6. **Analyzing Data:**
- The script then groups and analyzes data by team, section, and individual performance, and saves the results to text files and visualizations to PNG files.

7. **Saving Outputs:**
- Analysis results are saved in the `text_data` folder, and visualizations are saved in the `images` folder.

By following this approach, you will have a comprehensive DataFrame that allows you to analyze each student's performance across all curriculum blocks, and you will be able to generate and save detailed reports and visualizations for your analysis.
