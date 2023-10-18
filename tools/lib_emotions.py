from em_st_artifacts import emotional_math
from em_st_artifacts.emotional_math import EmotionalMath
from em_st_artifacts.utils.lib_settings import (ArtifactDetectSetting, MathLibSetting, MentalAndSpectralSetting, ShortArtifactDetectSetting, )

def init_paramters():
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

init_paramters()

