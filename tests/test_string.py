

def test_if_string_is_substring():
    s1 = "bar"
    s2 = "foobar"
    hitcounter = 0

    for c in s2:
        if c == s1[hitcounter]:
            hitcounter = hitcounter + 1
        elif (hitcounter > 0) and (c != s1[hitcounter]):
            hitcounter = 0
        if hitcounter == len(s1):
            print("found")
            return            
    print ("not found")
