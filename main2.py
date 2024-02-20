def replace_duplicate_characters(input_str, k):
    result = list(input_str)
    
    for i in range(len(input_str)):
        current_char = input_str[i]
        if current_char in input_str[max(i - k, 0):i]:
            result[i] = '-'
    
    return ''.join(result)

if __name__ == "__main__":
    input_str1 = "abcdefaxc"
    k1 = 10
    output_str1 = replace_duplicate_characters(input_str1, k1)
    print("Input:", input_str1, k1)
    print("Output:", output_str1)

    input_str2 = "abcdefaxcqwertba"
    k2 = 10
    output_str2 = replace_duplicate_characters(input_str2, k2)
    print("Input:", input_str2, k2)
    print("Output:", output_str2)