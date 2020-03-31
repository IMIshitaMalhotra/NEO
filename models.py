class NearEarthObject(object):
    """
    Object containing data describing a Near Earth Object and it's orbits.

    # TODO: You may be adding instance methods to NearEarthObject to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given Near Earth Object, only a subset of attributes used
        """
        
        self.id=kwargs.get('neo_id')
        self.name=kwargs.get('name')
        self.diameter_min_km=kwargs.get('min_d')
        self.diameter_max_km=kwargs.get('max_d')
        self.is_potentially_hazardous_asteroid=kwargs.get('is_hazardous')
        self.orbits=list()

    def update_orbits(self, orbit):
        """
        Adds an orbit path information to a Near Earth Object list of orbits

        :param orbit: OrbitPath
        :return: None
        """

        self.orbits.append(orbit)
    
    def __str__(self):
        orbits=','.join([orbit.get_basic_details() for orbit in self.orbits])
        
        return "NAME: "+self.name+" ID: "+str(self.id)+" ORBITS --> "+orbits

class OrbitPath(object):
    """
    Object containing data describing a Near Earth Object orbit.

    # TODO: You may be adding instance methods to OrbitPath to help you implement search and output data.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs:    dict of attributes about a given orbit, only a subset of attributes used
        """
        self.neo_name=kwargs.get('name')
        self.speed=kwargs.get('speed')
        self.miss_distance_kilometers=kwargs.get('miss_d')
        self.close_approach_date=kwargs.get('date')
        self.orbiting_body=kwargs.get('orbiting_body')
    
    def __str__(self):
        return "NEO NAME: "+self.neo_name+" @ "+self.close_approach_date+" BY "+self.miss_d
    
    def get_basic_details(self):
        return self.neo_name+" @ "+self.close_approach_date
