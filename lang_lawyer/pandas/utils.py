
def sanitize_column_names(df, inplace=True):
    "Replace all non-identifier characters in column names with _."
    def sanit(name):
        name = name.lower()
        name = re.sub('\W', '_', name)
        name = re.sub('__+', '_', name)
        name = re.sub('(?<=.)_$', '', name) # positive lookbehind assertion (group)
        return name

    if not inplace:
        df = df.copy()
    df.columns = [sanit(col) for col in df.columns]
    return df


def are_dependent_columns(df, left, right):
    """Check if one group of columns (or single column) always repeats like another."""
    left_idx = df.set_index(left).index
    right_idx = df.set_index(right).index

    return (left_idx.factorize()[0] == right_idx.factorize()[0]).all()

