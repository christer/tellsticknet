def decode(packet):
    """
    https://raw.githubusercontent.com/telldus/telldus/master/telldus-core/service/ProtocolOregon.cpp

    >>> decode(dict(data=0x201F242450443BDD, model=6701))["data"]["temp"]
    24.2
    >>> decode(dict(data=0x201F242450443BDD, model=6701))["data"]["humidity"]
    45.0
    """

    if int(packet["model"], 16) == 0x1a2d:
        return decode1A2D(packet)

    if int(packet["model"], 16) == 0xf824:
        return decodeF824(packet)

    raise NotImplementedError(
        "The Oregon model %s is not implemented. Data was %s" % (str(packet["model"]), str(packet["data"]))
    )

def decode1A2D(packet):
    data = packet["data"]
    value = int(data)
    value >>= 8
    checksum1 = value & 0xFF
    value >>= 8

    checksum = ((value >> 4) & 0xF) + (value & 0xF)
    hum1 = value & 0xF
    value >>= 8

    checksum += ((value >> 4) & 0xF) + (value & 0xF)
    neg = value & (1 << 3)
    hum2 = (value >> 4) & 0xF
    value >>= 8

    checksum += ((value >> 4) & 0xF) + (value & 0xF)
    temp2 = value & 0xF
    temp1 = (value >> 4) & 0xF
    value >>= 8

    checksum += ((value >> 4) & 0xF) + (value & 0xF)
    temp3 = (value >> 4) & 0xF
    value >>= 8

    checksum += ((value >> 4) & 0xF) + (value & 0xF)
    address = value & 0xFF
    value >>= 8

    checksum += ((value >> 4) & 0xF) + (value & 0xF)
    checksum += 0x1 + 0xA + 0x2 + 0xD - 0xA

    if checksum != checksum1:
        raise ValueError(
            "The checksum in the Oregon packet does not match "
            "the caluclated one!"
        )

    temperature = ((temp1 * 100) + (temp2 * 10) + temp3) / 10.0
    if neg:
        temperature = -temperature

    humidity = (hum1 * 10.0) + hum2

    return dict(
        packet,
        sensorId=address,
        data=dict(temp=temperature, humidity=humidity),
    )


def decodeF824(packet):
    data = packet["data"]
    value = int(data)

    crcCheck = value & 0xF
    value >>= 4

    messageChecksum1 = value & 0xF
    value >>= 4
    messageChecksum2 = value & 0xF
    value >>= 4
    unknown = value & 0xF
    value >>= 4
    hum1 = value & 0xF
    value >>= 4
    hum2 = value & 0xF
    value >>= 4
    neg = value & 0xF
    value >>= 4
    temp1 = value & 0xF
    value >>= 4
    temp2 = value & 0xF
    value >>= 4
    temp3 = value & 0xF
    value >>= 4
    battery = value & 0xF  # PROBABLY battery
    value >>= 4
    rollingcode = ((value >> 4) & 0xF) + (value & 0xF)
    checksum = ((value >> 4) & 0xF) + (value & 0xF)
    value >>= 8
    channel = value & 0xF
    checksum += unknown + hum1 + hum2 + neg + temp1 + temp2 + temp3 + battery + channel + 0xF + 0x8 + 0x2 + 0x4

    if ((checksum >> 4) & 0xF) != messageChecksum1 or (checksum & 0xF) != messageChecksum2:
        raise ValueError(
            "The checksum in the Oregon packet does not match "
            "the caluclated one!"
        )

    temperature = ((temp1 * 100) + (temp2 * 10) + temp3)/10.0
    if neg:
        temperature = -temperature
    
    humidity = (hum1 * 10.0) + hum2

    return dict(
        packet,
        sensorId=rollingcode,
        data=dict(temp=temperature, humidity=humidity),
    )
