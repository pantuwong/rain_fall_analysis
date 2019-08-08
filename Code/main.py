from modules import RainFallAnalyzer

if __name__ == '__main__':

    # create analyzer
    #rfa = RainFallAnalyzer.RainFallAnalyzer('C:\\Users\\Natapon Pantuwong\\Desktop\\\selected hydrological station')
    rfa = RainFallAnalyzer.RainFallAnalyzer('/home/.ecryptfs/napan/work/rain/selected hydrological station')
    
    rfa.calculate_average_rainfall_daily( rfa.station_name_list[2] )
    rfa.calculate_average_rainfall_monthly( rfa.station_name_list[2] )
    rfa.calculate_average_rainfall_yearly( rfa.station_name_list[2] )