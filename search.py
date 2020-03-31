from collections import namedtuple
from enum import Enum
from operator import *
from exceptions import UnsupportedFeature
from models import NearEarthObject, OrbitPath
import copy
import datetime


class DateSearch(Enum):
    """
    Enum representing supported date search on Near Earth Objects.
    """
    between = 'between'
    equals = 'equals'

    @staticmethod
    def list():
        """
        :return: list of string representations of DateSearchType enums
        """
        return list(map(lambda output: output.value, DateSearch))


class Query(object):
    """
    Object representing the desired search query operation to build. The Query uses the Selectors
    to structure the query information into a format the NEOSearcher can use for date search.
    """

    Selectors = namedtuple('Selectors', ['date_search', 'number', 'filters', 'return_object'])
    DateSearch = namedtuple('DateSearch', ['type', 'values'])
    ReturnObjects = {'NEO': NearEarthObject, 'Path': OrbitPath}

    def __init__(self, **kwargs):
        """
        :param kwargs: dict of search query parameters to determine which SearchOperation query to use
        """
        
        self.output=kwargs.get('output')
        self.return_object=kwargs.get('return_object')
        self.date=kwargs.get('date')
        self.start_date=kwargs.get('start_date')
        self.end_date=kwargs.get('end_date')
        self.number=kwargs.get('number')
        self.filter=kwargs.get('filter')
        

    def build_query(self):
        """
        Transforms the provided query options, set upon initialization, into a set of Selectors that the NEOSearcher
        can use to perform the appropriate search functionality

        :return: QueryBuild.Selectors namedtuple that translates the dict of query options into a SearchOperation
        """
        
        if self.date==None:
            date_type=DateSearch.between
            value=[self.start_date,self.end_date]
        else:
            date_type=DateSearch.equals
            value=self.date
            
        if self.filter != None:
            filters=Filter.create_filter_options(self.filter)
        else:
            filters=None
        return_object = Query.ReturnObjects['NEO'] if self.return_object=='NEO' else Query.ReturnObjects['Path']
        date_search=Query.DateSearch(date_type,value)
        selectors=Query.Selectors(date_search,self.number,filters,return_object)
        # TODO: Translate the query parameters into a QueryBuild.Selectors object
        
        return selectors
        


class Filter(object):
    """
    Object representing optional filter options to be used in the date search for Near Earth Objects.
    Each filter is one of Filter.Operators provided with a field to filter on a value.
    """
    Options = {
        # TODO: Create a dict of filter name to the NearEarthObject or OrbitalPath property
        'is_hazardous' :[NearEarthObject,'is_potentially_hazardous_asteroid'],
        'diameter' : [NearEarthObject,'diameter_min_km'],
        'distance' : [OrbitPath,'miss_distance_kilometers']
    }

    Operators = {
        # TODO: Create a dict of operator symbol to an Operators method, see README Task 3 for hint
        '=' :eq,
        '>=' :ge,
        '<=' :le,
        '<' :lt,
        '>' :gt,
        
    }

    def __init__(self, field, object, operation, value):
        """
        :param field:  str representing field to filter on
        :param operation: str representing filter operation to perform
        :param value: str representing value to filter for
        """
        self.field = field
        self.object = object
        self.operation = operation
        self.value = value

    @staticmethod
    def create_filter_options(filter_options):
        """
        Class function that transforms filter options raw input into filters

        :param input: list in format ["filter_option:operation:value_of_option", ...]
        :return: defaultdict with key of NearEarthObject or OrbitPath and value of empty list or list of Filters
        """
        defaultdict={
            "NearEarthObject":[],
            "OrbitPath":[]
            }
        
        for options in filter_options:
            filter_data=options.split(':')
            if Filter.Options[filter_data[0]][0].__name__=="NearEarthObject":
                filter_object=Filter(Filter.Options[filter_data[0]][1],NearEarthObject,Filter.Operators[filter_data[1]],filter_data[2])
                defaultdict["NearEarthObject"].append(filter_object)
            else:
                filter_object=Filter(Filter.Options[filter_data[0]][1],OrbitPath,Filter.Operators[filter_data[1]],filter_data[2])
                defaultdict["OrbitPath"].append(filter_object)
            
        return defaultdict
        # TODO: return a defaultdict of filters with key of NearEarthObject or OrbitPath and value of empty list or list of Filters

    def apply(self, results):
        """
        Function that applies the filter operation onto a set of results

        :param results: List of Near Earth Object results
        :return: filtered list of Near Earth Object results
        """
        result_list=list()
        if self.object.__name__=='NearEarthObject':
            #print("Filter of ",self.field,self.value,self.operation)
            for item in results:
                #print("item of",getattr(item,self.field),self.value,self.operation(str(getattr(item,self.field)),str(self.value)))
                if self.operation(str(getattr(item,self.field)),str(self.value)):
                    result_list.append(item)
        else:
            #print("Filter of ",self.field,self.value,self.operation)
            for item in results:
                orbit_list=list()
                for orbit in item.orbits:
                    #print("items of",getattr(item,self.field),self.value)
                    if self.operation(str(getattr(orbit,self.field)),str(self.value)):
                        orbit_list.append(orbit)
                if len(orbit_list)!=0:
                    item.orbits=orbit_list
                    result_list.append(item)
                    
        
        return result_list
        # TODO: Takes a list of NearEarthObjects and applies the value of its filter operation to the results


class NEOSearcher(object):
    """
    Object with date search functionality on Near Earth Objects exposed by a generic
    search interface get_objects, which, based on the query specifications, determines
    how to perform the search.
    """

    def __init__(self, db):
        """
        :param db: NEODatabase holding the NearEarthObject instances and their OrbitPath instances
        """
        self.db = db
        # TODO: What kind of an instance variable can we use to connect DateSearch to how we do search?

    def get_objects(self, query):
        """
        Generic search interface that, depending on the details in the QueryBuilder (query) calls the
        appropriate instance search function, then applys any filters, with distance as the last filter.

        Once any filters provided are applied, return the number of requested objects in the query.return_object
        specified.

        :param query: Query.Selectors object with query information
        :return: Dataset of NearEarthObjects or OrbitalPaths
        """
        #initializing
        results=list()
        #date results
        
        if query.date_search.type==DateSearch.between:
            st_d=[int(date) for date in query.date_search.values[0].split('-')]  #start date
            st_d=datetime.datetime(st_d[0],st_d[1],st_d[2])
            ed_d=[int(date) for date in query.date_search.values[1].split('-')]  #end date
            ed_d=datetime.datetime(ed_d[0],ed_d[1],ed_d[2])
            
            for neo_date in self.db.neos_by_date.keys():
                date=[int(date) for date in neo_date.split('-')]
                date=datetime.datetime(2000+date[2],date[1],date[0])
                if date>=st_d and date<=ed_d:
                    #print(st_d,date,ed_d)
                    results.extend(self.db.neos_by_date[neo_date])
                
        else:
            s_d=[int(date) for date in query.date_search.values.split('-')]
            s_d=datetime.datetime(s_d[0],s_d[1],s_d[2])
            for neo_date in self.db.neos_by_date.keys():
                date=[int(date) for date in neo_date.split('-')]
                date=datetime.datetime(2000+date[2],date[1],date[0])
                if s_d == date:
                    #print(date,s_d)
                    results.extend(self.db.neos_by_date[neo_date])
        
        
        results=list(set(results))
        if query.filters!=None:
            #applying filters
            for filt in query.filters['NearEarthObject']:
                results=filt.apply(results)
            #print(len(results))
            for filt in query.filters['OrbitPath']:
                results=filt.apply(results)
            #print(len(results))
        
        # #applying numbers
        final_result=list()
        if len(results)==0:
            return []
        elif len(results)>query.number:
            for i in range(query.number):
                final_result.append(results[i])
        else:
            for i in range(len(results)):
                final_result.append(results[i])
        
        return final_result
        # TODO: This is a generic method that will need to understand, using DateSearch, how to implement search
        # TODO: Write instance methods that get_objects can use to implement the two types of DateSearch your project
        # TODO: needs to support that then your filters can be applied to. Remember to return the number specified in
        # TODO: the Query.Selectors as well as in the return_type from Query.Selectors
