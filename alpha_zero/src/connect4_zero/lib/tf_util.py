def set_session_config(per_process_gpu_memory_fraction=None, allow_growth=None):
    """

    :param allow_growth: When necessary, reserve memory
    :param float per_process_gpu_memory_fraction: specify GPU memory usage as 0 to 1

    :return:
    """
    import tensorflow as tf
    import keras.backend as K

    config = tf.ConfigProto(
        gpu_options=tf.GPUOptions(
            per_process_gpu_memory_fraction=per_process_gpu_memory_fraction,
            allow_growth=allow_growth,
        )
    )
    sess = tf.Session(config=config)
    K.set_session(sess)
