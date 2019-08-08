import os

import pandas as pd 
import matplotlib.pyplot as plt

import seaborn as sns


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
        self.daily_avg = None
        self.monthly_avg = None
        self.yearly_avg = None
        self.daily_peak = None
        
    def calculate_average_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_avg == None:
            self.daily_avg = {}
        
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
        
        if self.monthly_avg == None:
            self.monthly_avg = {}
        
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
        
        if self.yearly_avg == None:
            self.yearly_avg = {}
            
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

    def calculate_peak_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_peak == None:
            self.daily_peak = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        data = pd.read_csv( os.path.join( self.path, filename ) )
        
        # get all date
        date = data.Date.unique()
        
        # process data
        temp_data = {}
        for index, row in data.iterrows():
            data_date = row['Date']
            data_rain = row['Rain (mm)']
            
            if data_date not in temp_data.keys():
                temp_data[data_date] = float(data_rain)
            else:
                if float(data_rain) > temp_data[data_date]:
                    temp_data[data_date] = float(data_rain)
        
        # calculate average and put in dataframe
        date_list = []
        peak_list = []
        type_list = []
        for d in date:
            peak = temp_data[d]
            date_list.append( d )
            peak_list.append( peak )
            if peak <= 10:
                type_list.append('light')
            elif peak <= 30:
                type_list.append('moderate')
            elif peak <= 60:
                type_list.append('heavy')
            else:
                type_list.append('very heavy')
        
        # initial value
        df = pd.DataFrame(columns=['Date','Peak (mm)','Intensity'])
        df['Date'] = date_list
        df['Peak (mm)'] = peak_list
        df['Intensity'] = type_list
        
        # set dataframe to dictionary
        self.daily_peak[station_name] = df
        
        if not os.path.exists( os.path.join( self.path, 'result_csv') ):
            os.mkdir(os.path.join( self.path, 'result_csv') )       
        df.to_csv( os.path.join( self.path, 'result_csv', station_name+'_daily_peak.csv' ) )
         
    def seasonal_trend( self, station_name, year ):
        
        #   calculate monthly average
        if self.monthly_avg == None:
            self.calculate_average_rainfall_monthly( station_name )
        
        #   get monthy average dataframe
        df = self.monthly_avg[station_name]
        
        #   filter dataframe to be only the year
        df_filtered = pd.DataFrame(columns=['Month','Average (mm)'])
        filter_month = []
        filter_rain = []
        custom_pallete = {}
        for index, row in df.iterrows():
            month = row['Month']
            if str(year) in month:
                avg = row['Average (mm)']
                filter_month.append(month)
                filter_rain.append(avg)
                splt = month.split('/')
                m = int(splt[0])
                if m >= 6 and m <= 9:
                    custom_pallete[month] = 'b'
                else:
                    custom_pallete[month] = 'r'
        df_filtered['Month'] = filter_month
        df_filtered['Average (mm)'] = filter_rain
        
        #   plot
        plt.figure(figsize=(16,9), dpi=100)
        ax = sns.lineplot(x="Month", y="Average (mm)",  palette=custom_pallete, data=df_filtered)
        plt.xticks(rotation=45)
        plt.title('Seasonal Trend ('+str(year)+')')
        plt.axvspan(0, 5, facecolor='r', alpha=0.2)
        plt.axvspan(5, 8, facecolor='g', alpha=0.2)
        plt.axvspan(8, 12, facecolor='r', alpha=0.2)
  
        if not os.path.exists( os.path.join( self.path, 'result_png') ):
            os.mkdir(os.path.join( self.path, 'result_png') )     
        plt.savefig(  os.path.join( self.path, 'result_png', station_name+'_seasonal_trend_'+str(year)+'.png' ) )
        
 