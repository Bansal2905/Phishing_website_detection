from urllib.parse import urlparse
import re
import string
import numpy as np

class FeaturesOf():
    '''
    This class will be used to provide following features for a given URL:
        1. Host name length
        2. Number of forward slash in URL
        3. Number of dots in the host name of URL
        4. Number of words in host name
        5. Presence of special characters in host name
        6. Presence of IP address in URL
        7. Presence of Unicode characters in URL
        # 8. Top Level Domain
        9. Number of dots in path of the URL
        10. Presence of Hyphen in host name of URL
        11. URL length
        12. presence of https
        13. Presence of @ symbol in URL
    '''
    
    def __init__(self, URL=''):
        self.URL = URL
        self.host_name = self.get_host_name()
    
    def get_host_name(self):
        '''
        This function will return the host name extracted from URL (empty string if not extracted)
        '''
        if self.URL == '':
            return ''
        else:
            parsed_url = urlparse(self.URL)
            if parsed_url.hostname == None:
                path = parsed_url.path
                if path != None and path.find('/')!=-1:
                    return path[0:path.find('/')]
                else: return ''
            return parsed_url.hostname
    
    def host_name_length(self):
        return len(self.host_name)
    
    def num_of_words_from_hostname(self):
        if self.host_name == '':
            return 0
        else:
            pattern = r'\b\w+\b'
            matches = re.findall(pattern, self.host_name)
            return len(matches)
    
    def is_special_character_present(self, char_list):
        '''
        It returns true if special character is present. In the present context, the special 
        character will exclude '.' and '-' characters.
        '''
        if self.host_name == '':
            return False
        else:
            for ch in self.host_name:
                if ch in char_list:
                    if ch == '.' or ch == '-':
                        continue
                    else:
                        return True
        return False
    
    def get_TLD(self):
        '''
        Provide top level domain from a given host name.
        
        Eg. 'com' in 'www.google.com'
        '''
        if self.host_name == '':
            return ''
        else:
            if '.' not in self.host_name:
                return ''
            else:
                return self.host_name.split('.')[-1]
    
    def num_of_dots_in_host_name(self):
        if self.host_name == '' or '.' not in self.host_name:
            return 0
        else:
            return len(self.host_name.split('.'))-1
    
    def is_hyphen_in_host_name(self):
        if self.host_name == '':
            return False
        else:
            if '-' in self.host_name:
                return True
            else:
                return False
    
    def https_present(self):
        if 'https' in self.URL:
            return True
        else:
            return False
    
    def num_of_for_slash_in_URL(self):
        if self.URL == '' or '/' not in self.URL:
            return 0
        else:
            return len(self.URL.split('/'))-1
    
    def num_of_dots_in_URL(self):
        if self.URL == '' or '.' not in self.URL:
            return 0
        else:
            return len(self.URL.split('.'))-1
    
    def size_of_URL(self):
        return len(self.URL)
    
    def is_at_symbol_in_URL(self):
        if self.URL == '':
            return False
        else:
            if '@' in self.URL:
                return True
            else:
                return False
    
    def is_unicode_character_in_URL(self):
        for ch in self.URL:
            if ord(ch) > 127:
                return True
        return False
    
    def is_ip_address_in_URL(self):
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        match = re.search(ip_pattern, self.URL)
        return bool(match)
    
    def get_features(self, char_list):
        ### the list will have values in the order as presented in class doc above
        features_list = []
        ### host name length
        features_list.append(self.host_name_length())
        ### number of forward slash in url
        features_list.append(self.num_of_for_slash_in_URL())
        ### number of dots in host name
        features_list.append(self.num_of_dots_in_host_name())
        ### number of words in host name
        features_list.append(self.num_of_words_from_hostname())
        ### presence of special characters in host name
        features_list.append(self.is_special_character_present(char_list))
        ### presence of ip address in url
        features_list.append(self.is_ip_address_in_URL())
        ### presence of unicode characters in url
        features_list.append(self.is_unicode_character_in_URL())
        ### top level domain
        # features_list.append(self.get_TLD())
        ### number of dots in url
        features_list.append(self.num_of_dots_in_URL())
        ### presence of hyphen in host name
        features_list.append(self.is_hyphen_in_host_name())
        ### url length
        features_list.append(self.size_of_URL())
        ### presence of https
        features_list.append(self.https_present())
        ### presence of @ symbol in url
        features_list.append(self.is_at_symbol_in_URL())
        return features_list
    
    def get_URL(self):
        return self.URL
    
    def fetch_host_name(self):
        return self.host_name
        

def get_enriched_data(split):
    '''
    This function will return an enriched data frame consisting of original 
    features (url and label) along with features extracted by class FeaturesOf 
    as additional columns.
    '''
    raw_data = split.copy()
    columns_list = ['host_length', 'num_slash_url', 'num_dots_host', 'num_words_host', 'is_special_chars_host', 
                'is_ip_add_url', 'is_unicode_chars_url', 'num_dots_url', 'is_hyphen_url', 'url_legth',
               'is_https', 'is_atsymbol_url']
    features_list = []
    char_list = string.punctuation
    for ind in range(raw_data.shape[0]):
        url_obj = FeaturesOf(raw_data.iloc[ind]['URL'])
        features = url_obj.get_features(char_list)
        features_list.append(features)
    features_array = np.array(features_list, dtype=object)
    for ind, col_name in enumerate(columns_list):
        raw_data[col_name] = features_array[:, ind]
    ### convert number based columns to int, from object
    columns_ind = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    for ind in columns_ind:
        col = columns_list[ind]
        raw_data[col] = raw_data[col].astype(int)
    return raw_data

