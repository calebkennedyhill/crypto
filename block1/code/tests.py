from main import euclid_gcd

def test_euclid_gcd():
    assert euclid_gcd(0,0) == 0
    assert euclid_gcd(48,18) == 6
    assert euclid_gcd(0,5) == 5
    assert euclid_gcd(22,0) == 22
    assert euclid_gcd(-4,88) == 4
    assert euclid_gcd(0,-63) == 63
    assert euclid_gcd(-675, 0) == 675
    assert euclid_gcd(1000000007, 998244353) == 1



from main import ext_gcd

def test_ext_gcd():
    assert ext_gcd(0,0) == (0,0,0)
    assert ext_gcd(240, 46) == (-9, 47, 2)
    assert ext_gcd(-46, 240) == (-47, -9, 2)
    assert ext_gcd(0, 0) == (0, 0, 0)
    assert ext_gcd(7, 0) == (1, 0, 7)
    assert ext_gcd(0, -99) == (0, -1, 99)



from main import crt

def test_crt():
    assert crt([1,1],[2,3]) == (1, 6)
    assert crt([2,3,2],[3,5,7]) == (23, 105) 
    assert crt([0,0],[4,9]) == (0, 36) 
    assert crt([4,13,1],[9,25,7]) == (463, 1575) 
    assert crt([5],[12]) == (5, 12) 
    assert crt([-1,-1],[4,9]) ==  (35, 36) 
    # assert crt([1,2],[4,6]) raises ValueError