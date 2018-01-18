import pickle;

BASE_CACHE_PATH = ".cache/";
def retreive_from_cache(unique_data_identifier): ## returns data or throws error if file does not exist in cache
    with open(BASE_CACHE_PATH + unique_data_identifier + ".pkl", 'rb') as f:
        data = pickle.load(f)
    return data;

def save_to_cache(unique_data_identifier, data):
    with open(BASE_CACHE_PATH + unique_data_identifier + ".pkl","wb") as f:
        pickle.dump(data, f);
