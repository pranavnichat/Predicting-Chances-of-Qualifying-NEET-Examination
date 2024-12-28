import pandas as pd
import numpy as np

# Define the categories and their corresponding probabilities
categories = ['GEN', 'OBC', 'SC', 'ST', 'NT', 'EWS']
category_probabilities = [0.3, 0.2, 0.15, 0.1, 0.1, 0.15]

# Define the range for NEETFinalScore
neet_final_score_min = 125
neet_final_score_max = 700

# Generate a dataset with approximately 400 records
num_records = 1000
np.random.seed(0)

# Initialize an empty DataFrame
data = pd.DataFrame(columns=['Test1', 'Test2', 'Test3', 'Test4', 'Test5', 'Test6', 'Test7', 'Test8', 'Test9', 'Test10', 'Category', 'NeetFinalScore'])

# Generate data for each record
for _ in range(num_records):
    # Generate mock test scores for Test1 to Test10
    test_scores = np.random.randint(0, 721, size=10)
    
    # Calculate the NEET final score based on the marks of the last three tests (Test8, Test9, and Test10)
    neet_final_score = np.sum(test_scores[-3:])
    
    # Add some variability to NEETFinalScore within the specified range
    neet_final_score = np.random.randint(neet_final_score_min, neet_final_score_max + 1)
    
    # Append the data to the DataFrame
    data = data._append({'Test1': test_scores[0], 'Test2': test_scores[1], 'Test3': test_scores[2],
                        'Test4': test_scores[3], 'Test5': test_scores[4], 'Test6': test_scores[5],
                        'Test7': test_scores[6], 'Test8': test_scores[7], 'Test9': test_scores[8],
                        'Test10': test_scores[9],  
                        'Category': np.random.choice(categories, p=category_probabilities), 
                        'NeetFinalScore': neet_final_score}, 
                       ignore_index=True)

# Save the generated dataset to a CSV file
data.to_csv('RESdataset.csv', index=False)
