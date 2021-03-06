#import q
import kdb
from collections import OrderedDict
import pandas as pd
import ipdb


def kdblogin(port=5000):
    '''
    shortcut to connect to q server

    Parameters
    ----------
    port: int
        the port number of Q process

    Returns
    -------
    object:
        the object to connect to Q process
    '''
    return kdb.q("localhost",port,"")

def qtable2df(qtable):
    '''
    Transfer qtable to pandas dataframe;
    '''
    # add a function to set time as data frame index
    colnames = qtable.x
    n = len(colnames)
    value = qtable.y
    interdict = OrderedDict()
    for i in range(n):
        interdict[colnames[i]] = value[i]

    return pd.DataFrame(interdict)

class dataloader(object):
    '''
    Data loader for KDB
    '''

    def __init__(self):
        '''
        initialization of data loader
        '''
        self.conn = kdblogin()

    def qload(self,command):

        '''
        load data from different database and return as pd time series
        field is a list of required fields

        Parameters
        ----------
        command : string
            Q-sql command send to kdb database

        Returns
        -------
        result : DataFrame
            Data received from KDB
        '''

        result = qtable2df(self.conn.k(command))
        if 'time' in result.columns:
            result.index = result['time']

        return result

    def qDirective(self, directive):
        '''
        Execute q directive in Q process
        '''
        self.conn.k(directive)

    def tickerload(self,source,symbol,beginDate,endDate = None):
        '''
        load corresponding data as df
        '''

        if endDate == None:
            endDate = beginDate

        range = '(' + beginDate + ';' + endDate + ')'

        if source != symbol:
            command = 'select from ' + source + ' where date within ' + range + ',symbol = `' + symbol.upper()
        else:
            command = 'select from ' + source + ' where date within ' + range

        return self.qload(command)




