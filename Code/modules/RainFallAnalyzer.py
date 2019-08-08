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
        ''' This function calculates average rainfall daily
        '''
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        data = pd.read_csv( os.path.join( self.path, filename ) )
        
        # get all date
        date = data.Date.unique()
        
        # count date
        count = data.Date.value_counts()
        
        # process data
        temp_data = {}
        for index, row in data.iterrows():
            data_date = row['Date']
            data_rain = row['Rain (mm)']
            
            if data_date not in temp_data.keys():
                temp_data[data_date] = float(data_rain)
            else:
                temp_data[data_date] += float(data_rain)
        
        # calculate average and put in dataframe
        date_list = []
        avg_list = []
        for d in date:
            avg = temp_data[d]/count[d]
            date_list.append( d )
            avg_list.append( avg )
        
        # initial value
        df = pd.DataFrame(columns=['Date','Average (mm)'])
        df['Date'] = date_list
        df['Average (mm)'] = avg_list
        
        # set dataframe to dictionary
        self.daily_avg[station_name] = df
        
        if not os.path.exists( os.path.join( self.path, 'result_csv') ):
            os.mkdir(os.path.join( self.path, 'result_csv') )       
        df.to_csv( os.path.join( self.path, 'result_csv', station_name+'_daily_avg.csv' ) )
    
    def calculate_average_rainfall_monthly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        data = pd.read_csv( os.path.join( self.path, filename ) )
            
        # process data
        temp_data = {}
        count_data = {}
        month = []
        for index, row in data.iterrows():
            data_date = row['Date']
            date_info = data_date.split('/')
            data_month = date_info[1]+'/'+date_info[2]
            if data_month not in month:
                month.append(data_month)
            data_rain = row['Rain (mm)']
            
            if data_date not in temp_data.keys():
                temp_data[data_month] = float(data_rain)
                count_data[data_month] = 1
            else:
                temp_data[data_month] += float(data_rain)
                count_data[data_month] += 1
        
        # calculate average and put in dataframe
        avg_list = []
        for m in month:
            avg = temp_data[m]/count_data[m]
            avg_list.append( avg )
        
        # initial value
        df = pd.DataFrame(columns=['Month','Average (mm)'])
        df['Month'] = month
        df['Average (mm)'] = avg_list
        
        # set dataframe to dictionary
        self.monthly_avg[station_name] = df
        
        if not os.path.exists( os.path.join( self.path, 'result_csv') ):
            os.mkdir(os.path.join( self.path, 'result_csv') )
        df.to_csv( os.path.join( self.path, 'result_csv', station_name+'_monthly_avg.csv' ) )       
            
    def calculate_average_rainfall_yearly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        data = pd.read_csv( os.path.join( self.path, filename ) )
            
        # process data
        temp_data = {}
        count_data = {}
        year = []
        for index, row in data.iterrows():
            data_date = row['Date']
            date_info = data_date.split('/')
            data_year = date_info[2]
            if data_year not in year:
                year.append(data_year)
            data_rain = row['Rain (mm)']
            
            if data_date not in temp_data.keys():
                temp_data[data_year] = float(data_rain)
                count_data[data_year] = 1
            else:
                temp_data[data_year] += float(data_rain)
                count_data[data_year] += 1
        
        # calculate average and put in dataframe
        avg_list = []
        for y in year:
            avg = temp_data[y]/count_data[y]
            avg_list.append( avg )
        
        # initial value
        df = pd.DataFrame(columns=['Year','Average (mm)'])
        df['Year'] = year
        df['Average (mm)'] = avg_list
        
        # set dataframe to dictionary
        self.yearly_avg[station_name] = df
        
        if not os.path.exists( os.path.join( self.path, 'result_csv') ):
            os.mkdir(os.path.join( self.path, 'result_csv') )
        df.to_csv( os.path.join( self.path, 'result_csv', station_name+'_yearly_avg.csv' ) )            
        
        
 