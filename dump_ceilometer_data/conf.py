
import ConfigParser

class CONF(object):
    """ CONF class is used to parse the configuration file.

    Typical use:
    try:
        conf = CONF(file)
    except Exception as e:
        print e
        sys.exit(1)

    """
    def __init__(self, configFile):
        try:
            self._get_config(configFile)
        except:
            raise

    def _get_config(self, configFile):
        configParser = ConfigParser.RawConfigParser()
        if configParser.read(configFile) == []:
            raise ValueError("Configuration file not found: " + configFile)

        try:
            self.c_version = configParser.getint('Ceilometer', 'version')
            self.username = configParser.get('Ceilometer', 'username')
            self.password = configParser.get('Ceilometer', 'password')
            self.auth_url = configParser.get('Ceilometer', 'auth_url')
            self.project_name = configParser.get('Ceilometer', 'project_name')

            self.request_limit = configParser.getint('Default', 'request_limit')
            self.start_timestamp = configParser.get('Default', 'start_timestamp')
            self.end_timestamp = configParser.get('Default', 'end_timestamp')

            
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
            raise ValueError("Configuration parsing error: " + str(e))
            
