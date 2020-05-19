import tools.signature_data_reader_cuba as reader
import tools.signature_data_normalizer_cuba as normalizer
import tools.signature_data_preprocessing_cuba as preprocessor
import tools.dtw_cuba as dtw
import tools.data_pickler_cuba as pickle

"""
I switched the arrays to dictionaries so we can iterate through them using the user-labels (001 - 030)

    the structure of the signature feature data dictionaries looks like this:
        dict = {"001": [signature_feature_array_1 ... signature_feature_array_N, "002": [singature_feature_array_1 ...
    
    
    the dtw dissimilarity array has following structure:
        dict = {"001": np.array([[e0v0, e1v0, e2v0, e3v0, e4v0, e5v0]  , "002": np.array([[e0v0, e1v0, e2v0, e3v0...
                                                    ....                                                     ....
                                 [e0vN, e1vN, e2vN, e3vN, e4vN, e5vN]]                    [e0vN, e1vN, e2vN, e3vN...
"""

if __name__ == '__main__':

    """ ### first we decide if we want to recompute our data ### """

    recompute_data = False  # set to true to recompute data, otherwise load pickled data

    if recompute_data:

        """ ### this chapter manages loading and processing our data ### """

        # Load Data
        dict_raw_enrollment_data, dict_raw_verification_data, dict_gt_labels = reader.read_data("./data/")

        # Process our 7 feature arrays to 5 feature arrays (with awesome new features)
        dict_enrollment_data = preprocessor.preprocess(dict_raw_enrollment_data)
        dict_verification_data = preprocessor.preprocess(dict_raw_verification_data)

        # Normalize values of our arrays for smoother dtw action
        dict_enrollment_norm, dict_verification_norm = normalizer.normalize(dict_enrollment_data, dict_verification_data)

        """ ### this chapter manages the steps where we actively rely on a dtw algorithm ### """

        # dtw time, get the 1st standard deviation quantiles for the dissimilarities within users!
        print("\n", "Calculating variance and mean within users")
        dict_mean, dict_variance, dict_1sd_intervals = dtw.calculate_variance_within_users(dict_enrollment_norm)
        pickle.save(dict_mean, "dict_mean")
        pickle.save(dict_variance, "dict_variance")
        pickle.save(dict_1sd_intervals, "dict_1sd_intervals")

        # now get the dissimilarity indices between all enrollment signatures and their verification signatures!
        print("\n", "Calculating dissimilarities between datasets")
        dict_dissimilarities = dtw.calculate_dissimilarities_between_datasets(dict_enrollment_norm, dict_verification_norm)
        pickle.save(dict_dissimilarities, "dict_dissimilarities")

    else:
        dict_mean = pickle.load("dict_mean")
        dict_variance = pickle.load("dict_variance")
        dict_1sd_intervals = pickle.load("dict_1sd_intervals")
        dict_dissimilarities = pickle.load("dict_dissimilarities")


    """ ### this chapter deals with the evaluation of our dtw data ### """

    # WIP todo @evaluation team
    print(dict_dissimilarities)