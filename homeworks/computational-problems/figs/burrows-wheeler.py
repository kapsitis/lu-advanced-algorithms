def build_suffix_array(text):
    """Builds suffix array for the given text."""
    suffixes = [(text[i:], i) for i in range(len(text))]
    sorted_suffixes = sorted(suffixes)
    suffix_array = [suffix[1] for suffix in sorted_suffixes]
    return suffix_array

def burrows_wheeler_transform(text):
    """Constructs Burrows-Wheeler Transform from given text."""
    n = len(text)
    # Get suffix array for the text
    suffix_array = build_suffix_array(text)
    # Create BWT using the suffix array
    bwt_result = ''.join(text[i-1] if i != 0 else text[-1] for i in suffix_array)
    return bwt_result

# Example usage
text = "MISSISSIPPI$"
bwt_result = burrows_wheeler_transform(text)
print("BWT of {}: {}".format(text, bwt_result))