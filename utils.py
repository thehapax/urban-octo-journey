
# remove all content that is SPONSORED
def split_sponsored(msg):
    if "SPONSORED" in msg:
        marr = msg.split("SPONSORED")
        return marr[0]
    else:
        return msg


if __name__ == "__main__":

    
    f = open("sample.txt", "r")
    content = f.read()

    result  = split_sponsored(content)
    print(result)
