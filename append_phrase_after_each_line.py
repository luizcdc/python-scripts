def append_DNS_list(file,
                    prase="··· no official Internet DNS name ···\n"):
    """
    Apply some treatment for a dns server ip list, so that the list could be
    parsed by a particular dns benchmarking application.
    """
    with open(file,"r") as source:
        slines = source.readlines()
    with open(file,"w") as ap:
        for ip in slines:
            ip = ip[:-1]
            ap.write(ip)
            for x in range(0, (30 - len(ip)) ):
                ap.write(" ")
            ap.write(prase)

if __name__ == "__main__":
    append_DNS_list("a.txt")
