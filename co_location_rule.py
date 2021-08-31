import pandas as pd
import numpy as np
import haversine as hs
from itertools import combinations


class CoLocation:
    def __init__(self, initial_data):
        self.initial_data = initial_data    # initial_data must be a dataframe
                                            # the dataframe columns name should contain at least [ID, Category, Kecamatan, Latitude, and Longitude]
                                            # pay attention to the case

        self.df_distances = pd.DataFrame(columns=['Kecamatan', 'ID_1', 'Category 1','ID_2', 'Category 2', 'Distance'])

        
        # Below is the code for calculating the distance
        # All item are clustered by column name 'Kecamatan'
        # The combination is following nC2 calculations, hence this code just can calculate only 2 combinations
        # Combination will be formed based on all unique item in column name 'Category'
        # The finished calculation will be inside 'self.df_distances' dataframe
        
        for kecamatan in self.initial_data['Kecamatan'].unique():
            filter_kecamatan = self.initial_data['Kecamatan'] == kecamatan
            dummy_df_kecamatan = self.initial_data[filter_kecamatan]
            
            for combi_cat in list(combinations(dummy_df_kecamatan['Category'].unique(), 2)):
                cat_1, cat_2 = combi_cat
                df_cat_1 = dummy_df_kecamatan[dummy_df_kecamatan['Category'] == cat_1]
                df_cat_2 = dummy_df_kecamatan[dummy_df_kecamatan['Category'] == cat_2]

                for id_1 in list(df_cat_1['ID'].values):
                    for id_2 in list(df_cat_2['ID'].values):
                        point_1 = (df_cat_1[ df_cat_1['ID'] == id_1]['Latitude'].values[0], df_cat_1[ df_cat_1['ID'] == id_1]['Longitude'].values[0])
                        point_2 = (df_cat_2[ df_cat_2['ID'] == id_2]['Latitude'].values[0], df_cat_2[ df_cat_2['ID'] == id_2]['Longitude'].values[0])
                        
                        distance = hs.haversine(point_1, point_2)   # Distances are calculated using haversine distance
                        data = [kecamatan, id_1, cat_1, id_2, cat_2, distance]
                        self.df_distances = self.df_distances.append(pd.Series(data, index=self.df_distances.columns), ignore_index=True)
                        
        
        # This code is calculating the number of unique ID for every unique category
        self.df_datasets = pd.DataFrame(columns=['Category', 'Total ID'])
        for category in self.initial_data['Category'].unique():
            data = pd.Series(data=[category, self.initial_data[self.initial_data['Category'] == category]['ID'].nunique()], index=self.df_datasets.columns)
            self.df_datasets = self.df_datasets.append(data, ignore_index=True)
        
    def range_distance(self, distance_range):
        # Call this function to filter distances
        mask = self.df_distances['Distance'] <= distance_range
        self.df_filtered_distance = self.df_distances[mask]
    
    def count_co_location(self):
        # This function is calculating Participation Ratio for each combination category and the final Participation Index

        self.df_co_location = pd.DataFrame(columns=['Category 1', 'Category 2', 'PR 1', 'PR2', 'PI'])

        for combi in list(combinations(self.df_datasets['Category'], 2)):
            category_1, category_2 = combi
            dummy_df = self.df_filtered_distance[(self.df_filtered_distance['Category 1'] == category_1) & (self.df_filtered_distance['Category 2'] == category_2)]
            
            len_category_1 = dummy_df['ID_1'].nunique()
            len_category_2 = dummy_df['ID_2'].nunique()
            
            total_cat_1 = self.df_datasets[self.df_datasets['Category'] == category_1]['Total ID'].values[0]
            total_cat_2 = self.df_datasets[self.df_datasets['Category'] == category_2]['Total ID'].values[0]

            pr_1 = len_category_1 / total_cat_1
            pr_2 = len_category_2 / total_cat_2

            data = [category_1, category_2, pr_1, pr_2, min(pr_1, pr_2)]
            self.df_co_location = self.df_co_location.append(pd.Series(data, index=self.df_co_location.columns), ignore_index=True)
    
    def co_location_result(self):
        return self.df_co_location
    
    def co_location_pruned(self):
        return self.df_co_location[self.df_co_location['PI'] >= 0.5 ]