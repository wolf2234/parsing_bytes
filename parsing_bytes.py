import pytest

test_data = [("10FA0E00", {'field1': 'Low',
                           'field2': '00',
                           'field3': '01',
                           'field4': '00',
                           'field5': '00',
                           'field6': '01',
                           'field7': '00',
                           'field8': 'Very High',
                           'field9': '00',
                           'field10': '00'}),
             ("00DC1A00", {'field1': 'Low',
                           'field2': '00',
                           'field3': '00',
                           'field4': '00',
                           'field5': '00',
                           'field6': '00',
                           'field7': '01',
                           'field8': 'reserved',
                           'field9': '00',
                           'field10': '00'}),
             ("11ABF101", {'field1': 'reserved',
                           'field2': '00',
                           'field3': '01',
                           'field4': '00',
                           'field5': '01',
                           'field6': '01',
                           'field7': '00',
                           'field8': 'High',
                           'field9': '01',
                           'field10': '01'}),
             ]

# Format settings - array [sett_byte1 as dict {bit: [size, 'field_name']}, sett_byte2, sett_byte3, sett_byte4]
device_settings = [{0: [3, 'field1'],
                    3: [1, 'field2'],
                    4: [1, 'field3'],
                    5: [3, 'field4']},
                   {0: [1, 'field5'],
                    1: [1, 'field6'],
                    2: [1, 'field7'],
                    3: [3, 'field8'],
                    },
                   {0: [1, 'field9'],
                    5: [1, 'field10']
                    },
                   {}
                   ]

field1 = {'0': 'Low',
          '1': 'reserved',
          '2': 'reserved',
          '3': 'reserved',
          '4': 'Medium',
          '5': 'reserved',
          '6': 'reserved',
          '7': 'High',
          }
field4 = {'0': '00',
          '1': '10',
          '2': '20',
          '3': '30',
          '4': '40',
          '5': '50',
          '6': '60',
          '7': '70',
          }
field8 = {'0': 'Very Low',
          '1': 'reserved',
          '2': 'Low',
          '3': 'reserved',
          '4': 'Medium',
          '5': 'High',
          '6': 'reserved',
          '7': 'Very High',
          }


def get_data_from_payload(payload):
    list_bits = []
    parsed_data = {}
    for char in payload:
        binary_number = bin(int(char, 16)).split('b')[1]
        length_binary_number = len(binary_number)
        if length_binary_number < 4:
            zero_bit = '0' * (4-length_binary_number)
            bit = zero_bit + binary_number
            bit = bit.strip()
            list_bits.append(bit)
        else:
            bit = binary_number
            list_bits.append(bit)
    list_bits = [''.join(list_bits[index:index+2])[::-1] for index in range(0, len(list_bits), 2)]
    for index, sett_byte in enumerate(device_settings):
        for bit, size, field in [(key, *value) for key, value in sett_byte.items()]:
            key = str(int(list_bits[index][bit:bit+size][::-1], 2))
            if field == 'field1':
                parsed_data[field] = field1[key]
            elif field == 'field4':
                parsed_data[field] = field4[key]
            elif field == 'field8':
                parsed_data[field] = field8[key]
            else:
                parsed_data[field] = '0' + key
    return parsed_data


@pytest.mark.parametrize("payload, result", test_data)
def test_get_data_from_payload(payload, result):
    assert get_data_from_payload(payload) == result
