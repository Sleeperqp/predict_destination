import json
import random


def import_data(train_file_path='../../data/train_trip.csv', train_output_path="../../data/libsvm.train",
                test_output_path="../../data/libsvm.test"):
    train_file = open(train_file_path, "r")
    train_output = open(train_output_path, "w")
    test_outpu = open(test_output_path, "w")
    buffernum = 1
    num = 1

    for line in train_file:
        try:
            datas = json.loads(line)
            data = []
            # CALL_TYPE:         1
            data.append(ord(datas[1].lower()) - ord('a'))
            # TAXI_ID:           1
            data.append(datas[2])
            # DAY_TYPE
            data.append(ord(datas[3].lower()) - ord('a'))
            # time embedding:    4
            for i in datas[4]:
                data.append(int(i))
            # trip:  10*2 =     20
            for i in datas[5]:
                data.append(i[0])
                data.append(i[1])

            if random.randint(1, 100) < 75:
                train_output.write(str(datas[6]))

                i = 1
                for t in data:
                    train_output.write(" " + str(i) + ":" + str(t))
                    i += 1
                train_output.write("\n")
            else:
                test_outpu.write(str(datas[6]))

                i = 1
                for t in data:
                    test_outpu.write(" " + str(i) + ":" + str(t))
                    i += 1
                test_outpu.write("\n")

            buffernum += 1
            num += 1
            if buffernum > 10000:
                buffernum = 0
                test_outpu.flush()
                train_output.flush()
            if num > 200000:
                break
        except:
            print 'error line:', line


if __name__ == '__main__':
    import_data()
