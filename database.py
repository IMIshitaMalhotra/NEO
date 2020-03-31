from models import OrbitPath, NearEarthObject
import pandas as pd


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        self.neos_by_name=dict()
        self.neos_by_date=dict()
        self.filename=filename

    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename
        
        datafile=pd.read_csv(filename)
        
        for row in datafile.itertuples():
            #Reading Rows and creating instances
            instance=None
            if row.name not in self.neos_by_name:
                instance=NearEarthObject(neo_id=row.id,
                                             name=row.name,
                                             min_d=row.estimated_diameter_min_kilometers,
                                             max_d=row.estimated_diameter_max_kilometers,
                                             is_hazardous=row.is_potentially_hazardous_asteroid)
                self.neos_by_name[row.name]=instance
            else:
                instance=self.neos_by_name[row.name]
            
            orbit=OrbitPath(name=row.name,
                            speed=row.kilometers_per_hour,
                            miss_d=row.miss_distance_kilometers,
                            date=row.close_approach_date,
                            orbiting_body=row.orbiting_body)
            
            instance.update_orbits(orbit)
            
            
            if row.close_approach_date not in self.neos_by_date:
                 self.neos_by_date[row.close_approach_date]=list()
            
            self.neos_by_date[row.close_approach_date].append(instance)
                 
            
        
        return None
