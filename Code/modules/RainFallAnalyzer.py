import os
from datetime import datetime

import pandas as pd 
from openpyxl import load_workbook

import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np


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

def save_xls( dframe, path, sheet_name ):
    ''' This function save dataframe to excel file
    '''  
    if os.path.exists(path): 
        book = load_workbook(path)
        writer = pd.ExcelWriter(path, engine='openpyxl')
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        dframe.to_excel(writer, sheet_name, na_rep='N/A' )
        writer.save()
    else: 
        writer = pd.ExcelWriter(path)
        dframe.to_excel(writer, sheet_name, na_rep='N/A' )
        writer.save() 

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
        self.dataframe = None
        self.daily_avg = None
        self.monthly_avg = None
        self.yearly_avg = None
        self.daily_peak = None
        self.annual_sum = None
        self.scatter_plot_data = []
    
    def createYearMonthDay( self, station_name ):
        #creating YearMonthDay field for the ease of reporting and visualization
        self.dataframe[station_name]['YearMonthDay'] =  self.dataframe[station_name]['Date'].map(lambda date: str(10000*date.year + 100*date.month + date.day))
    
    def createYearMonth( self, station_name ):
        #creating YearMonthDay field for the ease of reporting and visualization
        self.dataframe[station_name]['YearMonth'] =  self.dataframe[station_name]['Date'].map(lambda date: str(100*date.year + date.month) )
    
    def calculate_average_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_avg == None:
            self.daily_avg = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )
            self.dataframe[station_name]['Date'] = self.dataframe[station_name]['Date'].map(lambda date: datetime.strptime(date,'%d/%m/%Y') ) 
            
            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )

        # calculate daily average
        tmp_df_daily_avg =  self.dataframe[station_name].groupby('YearMonthDay')['Rain (mm)'].mean().reset_index()
        tmp_df_daily_avg = tmp_df_daily_avg.round(2)
        tmp_df_daily_avg['Date'] = tmp_df_daily_avg['YearMonthDay'].map( lambda date: str(date)[6:8]+'/'+str(date)[4:6]+'/'+str(date)[:4]  )
        df_daily_avg = tmp_df_daily_avg[['Date','Rain (mm)']].copy()
        df_daily_avg.rename(columns={'Rain (mm)':'Daily Avg (mm)'}, inplace=True)

        # set dataframe to dictionary
        self.daily_avg[station_name] = df_daily_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )     
        
        save_xls( df_daily_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Daily Average' )
    
    def calculate_average_rainfall_monthly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        
        if self.monthly_avg == None:
            self.monthly_avg = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )
            self.dataframe[station_name]['Date'] = self.dataframe[station_name]['Date'].map(lambda date: datetime.strptime(date,'%d/%m/%Y') ) 

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )

        # calculate monthly average
        tmp_df_monthly_avg =  self.dataframe[station_name].groupby('YearMonth')['Rain (mm)'].mean().reset_index()
        tmp_df_monthly_avg = tmp_df_monthly_avg.round(2)
        tmp_df_monthly_avg['Month'] = tmp_df_monthly_avg['YearMonth'].map( lambda date: str(date)[4:6]+'/'+str(date)[:4]  )
        df_monthly_avg = tmp_df_monthly_avg[['Month','Rain (mm)']].copy()
        df_monthly_avg.rename(columns={'Rain (mm)':'Monthly Avg (mm)'}, inplace=True)
        
        # set dataframe to dictionary
        self.monthly_avg[station_name] = df_monthly_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )       

        save_xls( df_monthly_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Monthly Average' )

    def calculate_average_rainfall_yearly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        
        if self.yearly_avg == None:
            self.yearly_avg = {}
            
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )          
            self.dataframe[station_name]['Date'] = self.dataframe[station_name]['Date'].map(lambda date: datetime.strptime(date,'%d/%m/%Y') ) 

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )

        if station_name not in self.monthly_avg.keys():
            self.calculate_average_rainfall_monthly( station_name )
            
        # calculate monthly average
        tmp_df_yearly =  self.monthly_avg[station_name].copy()
        tmp_df_yearly['Date'] = tmp_df_yearly['Month'].map(lambda date: datetime.strptime(date,'%m/%Y') )
        tmp_df_yearly['Year'] = tmp_df_yearly['Date'].map(lambda date: str(date.year) )
        tmp_df_yearly_avg = tmp_df_yearly.groupby('Year')['Monthly Avg (mm)'].sum().reset_index()
        tmp_df_yearly_avg = tmp_df_yearly_avg.round(2)
        df_yearly_avg = tmp_df_yearly_avg[['Year','Monthly Avg (mm)']].copy()
        df_yearly_avg.rename(columns={'Monthly Avg (mm)':'Yearly Avg (mm)'}, inplace=True)
        
        # set dataframe to dictionary
        self.yearly_avg[station_name] = df_yearly_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )       

        save_xls( df_yearly_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Yearly Average' )


    def calculate_peak_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_peak == None:
            self.daily_peak = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )

        # calculate daily peak
        tmp_df_daily_peak =  self.dataframe[station_name].groupby('YearMonthDay')['Rain (mm)'].max().reset_index()
        tmp_df_daily_peak = tmp_df_daily_peak.round(2)
        tmp_df_daily_peak['Date'] = tmp_df_daily_peak['YearMonthDay'].map( lambda date: str(date)[6:8]+'/'+str(date)[4:6]+'/'+str(date)[:4]  )

        def intensity( val ):
            if val <= 10:
                return 'Light'
            elif val <= 30:
                return 'Moderate'
            elif val <= 60:
                return 'Heavey'
            else:
                return 'Very Heavey'

        tmp_df_daily_peak['Rain Intensity'] = tmp_df_daily_peak['Rain (mm)'].map( lambda val: intensity(val))
        df_daily_peak = tmp_df_daily_peak[['Date','Rain (mm)','Rain Intensity']].copy()
        df_daily_peak.rename(columns={'Rain (mm)':'Daily Peak (mm)'}, inplace=True)

        # set dataframe to dictionary
        self.daily_peak[station_name] = df_daily_peak
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )     
        
        save_xls( df_daily_peak, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Daily Peak' )

    def calculate_annual_sum( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        
        if self.annual_sum == None:
            self.annual_sum = {}
            self.scatter_plot_data = {}
            
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )          
            self.dataframe[station_name]['Date'] = self.dataframe[station_name]['Date'].map(lambda date: datetime.strptime(date,'%d/%m/%Y') ) 

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )

        if station_name not in self.monthly_avg.keys():
            self.calculate_average_rainfall_monthly( station_name )         
        
        # dictionary for summary data
        annual_sum_list = []
        processed_year = []
        scatter_plot = []

        # iterate in each row of monthly average
        for index, row in self.monthly_avg[station_name].iterrows():
            m = row['Month']
            r = row['Monthly Avg (mm)']

            scatter_plot.append([m,r])
            
            m_data = m.split('/')
            m = int(m_data[0])
            y = int(m_data[1])

            if y not in processed_year:
                initial_list = [y]
                initial_list.extend([np.nan for i in range(15)])
                annual_sum_list.append(initial_list)
                annual_sum_list[-1][m] = r
                processed_year.append(y)
            else:
                annual_sum_list[-1][m] = r
            
            if m == 12:
                winter_data = [annual_sum_list[-1][1], annual_sum_list[-1][2], annual_sum_list[-1][11], annual_sum_list[-1][12]] 
                if None in winter_data:
                    annual_sum_list[-1][13] = None
                else:
                    annual_sum_list[-1][13] = sum( winter_data )/4.0
                
                rainny_data = [annual_sum_list[-1][5], annual_sum_list[-1][6], annual_sum_list[-1][7], annual_sum_list[-1][8]]
                if None in rainny_data:
                    annual_sum_list[-1][14] = None
                else:
                    annual_sum_list[-1][14] = sum( rainny_data )/4.0
                
                if None in annual_sum_list[-1][1:13]:
                    annual_sum_list[-1][15] = None
                else:
                    annual_sum_list[-1][15] = sum( annual_sum_list[-1][1:13] )/12.0

        # create dataframe from list
        df = pd.DataFrame( annual_sum_list, columns = ['Year','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','NEM','SWM','Annual Avg'])
        df = df.round(2)
        self.annual_sum[station_name] = df
        sdf = pd.DataFrame( scatter_plot, columns = ['Month of Date', 'Average Rain (mm)'] )
        sdf = sdf.round(2)
        self.scatter_plot_data[station_name] = sdf

        # save to xlsx
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )     
        
        save_xls( df, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Annual Summary' )
    
    def create_scatter_plot( self, station_name ):
        ''' This function create scatter plot from each station
        '''

        if ( self.annual_sum == None ) or ( station_name not in self.annual_sum.keys() ):
            self.calculate_annual_sum( station_name )

        df = self.scatter_plot_data[station_name]
        df = df.round(2)
        xtick = []
        r = []
        for index, row in df.iterrows():
            m = row['Month of Date']
            m_data = m.split('/')
            m = int(m_data[0])
            if m == 1:
                xtick.append(int(m_data[1]))
            else:
                xtick.append('')
            r.append(row['Average Rain (mm)'])

        #build the plot
        plt.figure(figsize=(16,9))
        plot = sns.scatterplot("Month of Date", "Average Rain (mm)", data=df, hue='Average Rain (mm)')
        l = plot.legend_
        for t in l.texts :
            if t.get_text() !=  "Average Rain (mm)":
                t.set_text("{0:.2f}".format(float(t.get_text())))
        plot.set(ylabel='Average Rain(mm)', xlabel='Month of Date') #add labels

        plt.xticks(df['Month of Date'], xtick, rotation=90)
        plt.axhline(y=sum(r)/len(r),linestyle='--')
        plt.text(0,(sum(r)/len(r))+0.01,'Average')
        # save to png
        if not os.path.exists( os.path.join( self.path, 'result_png') ):
            os.mkdir(os.path.join( self.path, 'result_png') )  
        plt.savefig( os.path.join( self.path, 'result_png', station_name+'_scatter_plot.png' ), dpi = 300)
        
        
    def create_line_plot( self, station_name ):
        ''' This function create line plot for each station
        '''

        if ( self.annual_sum == None ) or ( station_name not in self.annual_sum.keys() ):
            self.calculate_annual_sum( station_name )
        
        df = self.annual_sum[station_name]
        xtick = []
        for index, row in df.iterrows():
            xtick.append(int(row['Year']))
        
        plt.figure(figsize=(16,9))
        plot = sns.lineplot(x="Year", y="Annual Avg", data=df )
        plot = plot.set(ylabel='Annaul Avg', xlabel='Year')

        plt.xticks(df['Year'],xtick,rotation=90)
        # save to png
        if not os.path.exists( os.path.join( self.path, 'result_png') ):
            os.mkdir(os.path.join( self.path, 'result_png') )  
        plt.savefig( os.path.join( self.path, 'result_png', station_name+'_line_plot.png' ), dpi = 300)


    def create_multi_line_plot( self ):
        ''' This function create multiple line plot for all station
        '''

        if ( self.annual_sum == None ):
            print('Cannot generate multi-line plot. Need to calculate data for at least 1 station first')
            return

        # create empty list
        data_list = []
        xtick = []

        # for each station name
        for station_name in self.station_name_list:

            if station_name not in self.annual_sum.keys():
                continue

            #  get dataframe
            data_frame = self.annual_sum[station_name]
            for index,row in data_frame.iterrows():
                if row['Year'] not in xtick:
                    xtick.append(row['Year'])
                data_list.append([row['Year'],station_name,row['Annual Avg']])
        
        xtick.sort()
    
        df = pd.DataFrame(data_list,columns=['Year','Station Name','Annual Avg'])
        plt.figure(figsize=(16,9))
        plot = sns.lineplot(x="Year", y="Annual Avg", hue='Station Name', data=df )
        plot = plot.set(ylabel='Annaul Avg', xlabel='Year')
        plt.xticks(rotation=90)

        if not os.path.exists( os.path.join( self.path, 'result_png') ):
            os.mkdir(os.path.join( self.path, 'result_png') )  
        plt.savefig( os.path.join( self.path, 'result_png', 'all_station_line_plot.png' ), dpi = 300)


            
