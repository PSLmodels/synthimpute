def rf_synth(X, seed_cols, n=None, trees=100, random_state=0):
    """Synthesize data via random forests.

    Args:
        X: Data to synthesize, as a pandas DataFrame.
        seed_cols: Columns to seed the synthesis, via sampling with replacement.
        n: Number of records to produce. Defaults to the number of records in X.
        trees: Number of trees in each model (n_estimators).
        random_state: Random state to use for initial sampling with replacement and random forest models.

    Returns:
        DataFrame with synthesized data.
    """
    # Start with the seed synthesis.
    if n is None:
        n = X.shape[0]
    synth = X.copy()[seed_cols].sample(n=n, replace=True, random_state=random_state)
    # Initialize random forests model object.
    rf = ensemble.RandomForestRegressor(n_estimators=trees,
                                        min_samples_leaf=1,
                                        random_state=random_state,
                                        n_jobs=-1)  # Use maximum number of cores.
    # Loop through each variable.
    rf_vars = list(set(X.columns) - set(seed_cols))
    for i, col in enumerate(rf_vars):
        print('Synthesizing feature ' + str(i + 1) + ' of ' +
              str(len(rf_vars)) + ': ' + col + '...')
        rf.fit(train[synth.columns], train[col])
        synth[col] = rf_quantile(rf, synth, np.random.rand(n))
    return synth
        