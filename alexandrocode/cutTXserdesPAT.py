# --uft8--
# cut serdes wave to sync&loop wave and complie to serdes PAT


# calc largest multiple
def lcm(m, n):
    if m == n:
        return m
    elif m > n:
        divisor = n
        dividend = m
    else:
        divisor = m
        dividend = n

    remainder = divisor % dividend

    while remainder > 0:
        divisor = dividend
        dividend = remainder
        remainder = divisor % dividend

    return m*n/dividend


if __name__ == "__main__":

    file_path = "C:\\Users\\gonghaiq\\Desktop\\1213_xuhua\\"
    file_name = "pma_tx1_7gx2_491m_bw400m.txt"
    pin_name = "gSDS_USRUL1_RF1_US10G_DRV"
    vm_vector_name = "Tx1_7gx2_491m_bw400m"

    serdes_rate = 7.3768 * (10**9)
    sample_rate = 122.88 * (10**6)
    offset = 2727

    # 84400 is least number of bits to repeat in US10G pattern
    # 84400 equals 11us in 7.3728g rate mode
    # least common divisor
    lcd = 84480
    '''sync 2ms'''
    sync_len = lcd * 174
    '''loop 2ms'''
    loop_len = lcd * 174

    with open(file_path + file_name, 'r') as f:
        content = f.read()
        content_stream = content.replace("\n", "")

    with open(file_path + file_name.replace(".txt", "_sync.txt"), "w") as f, \
         open(file_path + file_name.replace(".txt", "_part1.txt"), "w") as f1:

        f.write('digital_inst=Serial10G;\n')
        f.write('vm_vector ' + vm_vector_name + '_SYNC(' + pin_name + ')\n')
        f.write('{\n')

        for i in range(sync_len):
            f1.write(content_stream[i + offset] + "\n")
            if (i % 66) == 0:
                f.write("> " + content_stream[i + offset] + "; // " + str(i//66) + "\n")
            else:
                f.write("> " + content_stream[i + offset] + ";" + "\n")

        f.write('}')

    with open(file_path + file_name.replace(".txt", "_loop.txt"), "w") as f, \
         open(file_path + file_name.replace(".txt", "_part2.txt"), "w") as f1:

        f.write('digital_inst=Serial10G;\n')
        f.write('vm_vector ' + vm_vector_name + '_SYNC(' + pin_name + ')\n')
        f.write('{\n')

        for j in range(loop_len):
            f1.write(content_stream[j + sync_len + offset] + "\n")
            if (j % 66) == 0:
                f.write("> " + content_stream[j + sync_len + offset] + "; // " + str(j//66) + "\n")
            else:
                f.write("> " + content_stream[j + sync_len + offset] + ";" + "\n")

        f.write('}')

    print("conversion done !!!")

