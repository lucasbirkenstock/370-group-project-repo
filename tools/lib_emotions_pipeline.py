from em_st_artifacts import emotional_math
from em_st_artifacts.emotional_math import EmotionalMath
from em_st_artifacts.utils.lib_settings import (ArtifactDetectSetting, MathLibSetting, MentalAndSpectralSetting, ShortArtifactDetectSetting, )
from em_st_artifacts.utils.support_classes import RawChannelsArray, RawChannels

def pipeline():
    calibration_length = 0
    nwins_skip_after_artifact = 10

    mls = MathLibSetting(sampling_rate=250,
    process_win_freq=25,
    fft_window=1000,
    n_first_sec_skipped=4,
    bipolar_mode=False,
    channels_number=4,
    channel_for_analysis=3)

    ads = ArtifactDetectSetting(hanning_win_spectrum=True, num_wins_for_quality_avg=125)

    sads = ShortArtifactDetectSetting(ampl_art_extremum_border=25)

    mss = MentalAndSpectralSetting()

    emotions = EmotionalMath(mls, ads, sads, mss)
    emotions.set_calibration_length(calibration_length)
    emotions.set_mental_estimation_mode(False)
    emotions.set_skip_wins_after_artifact(nwins_skip_after_artifact)
    emotions.set_zero_spect_waves(True, 0, 1, 1, 1, 0)
    emotions.set_spect_normalization_by_bands_width(True)

    size = 1500

    # This is basically the pipeline, because it runs indefinitely 
    while True:
        #Raw data list
        raw_channels_list = []

        # I do not currently understand this section TODO
        for _ in range(size):
            raw_channels_list.append(RawChannels(3, 1))

        # Raw data is pushed to emotional math object and processed
        emotions.push_data(raw_channels_list)
        emotions.process_data_arr()

        # After the raw data is processed above, retrieve the data and store in vars
        mind_data_list = emotions.read_mental_data_arr()
        mind_data = emotions.read_average_mental_data(1)
        raw_spect_vals = emotions.read_raw_spectral_vals()
        percents = emotions.read_spectral_data_percents_arr()


        # I believe is_both_sides artifacted indicates signal corruption. Not entirely sure.
        if emotions.is_both_sides_artifacted():
            print()

        # Mind_data retrieves AVERAGE mental data
        print("Mind Data: {} {} {} {}".format(mind_data.rel_attention,
                                              mind_data.rel_relaxation,
                                              mind_data.inst_attention,
                                              mind_data.inst_relaxation))


        for i in range(emotions.read_mental_data_arr_size()):
            print("{}: {} {} {} {}".format(i,
                                           mind_data_list[i].rel_attention,
                                           mind_data_list[i].rel_relaxation,
                                           mind_data_list[i].inst_attention,
                                           mind_data_list[i].inst_relaxation))

        # Raw spectrum values
        print("Raw Spect Vals: {} {}".format(raw_spect_vals.alpha, raw_spect_vals.beta))

        for i in range(emotions.read_spectral_data_percents_arr_size()):
            print("{}: {} {} {} {} {}".format(i,
                                              percents[i].alpha,
                                              percents[i].beta,
                                              percents[i].gamma,
                                              percents[i].delta,
                                              percents[i].theta))


pipeline()

