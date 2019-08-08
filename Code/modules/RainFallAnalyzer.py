import os

import pandas as pd 

def get_filename_list( path ):
    ''' This function gets all .csv file in this path
    '''
    # set suffix to .csv
    suffix = ".csv"

    # list file in the path
    filenames = os.listdir( path )

    # return list of csv file
    return [ filename for filename in filenames if filename.endswith( suffix )]

def get_stationname_list( filename_list ):
    ''' This function extract station name from filename list
    '''
    return [ os.path.splitext( filename )[0] for filename in filename_list ]


''' This is the main module for rainfall analysis
'''
class RainFallAnalyzer:

    def __init__ ( self, csv_path ):
        ''' This is init function for the class
        '''
        # set path
        self.path = csv_path

        # get all file name
        self.data_filename_list = get_filename_list( csv_path )

        # get all station name (based on data_filename)
        self.station_name_list = get_stationname_list( self.data_filename_list ) 
        
        # define variables
        self.daily_avg = {}
        self.monthly_avg = {}
        self.yearly_avg = {}

    def calculate_average_rainfall_daily( self, station_name ):

        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        data = pd.read_csv( os.path.join( self.path, filename ) )
        
        # get all date
        date = data.Date.unique()
        
        # initial value
        self.daily_avg[station_name] = pd.DataFrame(columns=['Date','Average (mm)'])
        
        # process data
        temp_data = {}
        for index, row in data.iterrows():
            data_date = row['Date']
            data_rain = row['Rain (mm)']
            
            if data_date not in temp_data.keys():
                temp_data[data_date] = 0.0
            else:
                temp_data[data_date] += float(data_rain)
        
        # calculate average and put in dataframe
        for d in date:
            count = data[data['Date']==d].count()
            print(count)
            avg = float(temp_data[date])/count
            self.daily_avg[station_name].append({'Date':d,'Rain (mm)':avg})
            
        print(self.daily_avg[station_name])
            
            
        
        
 