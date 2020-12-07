# ---------------------------
# Advent of Code 2020 - Day 1
# Part 1: Report Repair
# ---------------------------

# After saving Christmas five years in a row, you've decided to take a
# vacation at a nice resort on a tropical island. Surely, Christmas will go
# on without you.

# The tropical island has its own currency and is entirely cash-only. The
# gold coins used there have a little picture of a starfish; the locals just
# call them stars. None of the currency exchanges seem to have heard of them,
# but somehow, you'll need to find fifty of these coins by the time you
# arrive so you can pay the deposit on your room.

# To save your vacation, you need to get all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on
# each day in the Advent calendar; the second puzzle is unlocked when you
# complete the first. Each puzzle grants one star. Good luck!

# Before you leave, the Elves in accounting just need you to fix your expense
# report (your puzzle input); apparently, something isn't quite adding up.

# Specifically, they need you to find the two entries that sum to 2020 and
# then multiply those two numbers together.

# For example, suppose your expense report contained the following:

# 1721 979 366 299 675 1456

# In this list, the two entries that sum to 2020 are 1721 and 299.
# Multiplying them together produces 1721 * 299 = 514579, so the correct
# answer is 514579.

# Of course, your expense report is much larger. Find the two entries that
# sum to 2020; what do you get if you multiply them together?



input = "1046 1565 1179 1889 1683 1837 1973 1584 1581 192 1857 1373 1715 1473 1770 1907 1918 1909 1880 1903 1835 1887 1511 1844 1628 1688 1545 1469 1620 1751 1893 1861 511 1201 1641 1874 1946 1701 1777 1829 1609 1805 1678 1928 1398 1555 1675 1798 1485 1911 1974 1663 1919 1635 195 1441 1525 1490 1151 1406 1408 1095 1085 1097 1976 1987 1498 1753 1603 1933 1729 1106 1929 1832 1744 1914 1643 1571 1391 1953 1790 1797 1938 258 1957 1858 1506 628 1109 1113 1768 1649 1669 694 1803 1849 1395 1754 1421 1575 1632 1998 1693 1499 1550 1771 1902 1801 1549 1459 1826 1927 1507 1718 647 1922 1432 1625 1904 1691 1427 1519 1949 1514 1749 1616 1898 1696 1917 1661 1787 1440 1796 1560 1956 1823 1815 1557 1730 1951 1548 1527 1881 1727 1530 1460 1360 1583 1662 1954 1890 1855 1752 1935 1601 1767 1812 1990 1445 1908 2001 1544 1814 1634 1532 1788 1521 1638 1470 1524 1394 1674 1314 1588 1429 1745 1416 1637 1942 484 1467 1764 1743 1401 1471 1458 1335 1866 1399 1393 1708 1694 1447 1972 1478 1182 1672 1813 1546 1535"

inputArr = sorted(map(int, input.split()))

def get_two_summands(arr, target):
    for i in range(len(inputArr)):
        for j in range(len(inputArr) - 1, i, -1):
            sum = inputArr[i] + inputArr[j]
            if(sum > target):
                continue
            elif(sum < target):
                break
            else:
                return [inputArr[i], inputArr[j]]
    raise Exception("There are no two numbers which add up to " + str(target))

print("2020 - Day 1 - Part 1")
try:
    [a, b] = get_two_summands(inputArr, 2020)
    print(a, "*", b, "=", a * b)
except Exception as e:
    print(str(e))

# => 647 * 1373 = 888331
#                 ======


# ---------------------------
# Advent of Code 2020 - Day 1
# Part 2: Report Repair
# ---------------------------

# The Elves in accounting are thankful for your help; one of them even offers
# you a starfish coin they had left over from a past vacation. They offer you
# a second one if you can find three numbers in your expense report that meet
# the same criteria.

# Using the above example again, the three entries that sum to 2020 are 979,
# 366, and 675. Multiplying them together produces the answer, 241861950.

# In your expense report, what is the product of the three entries that sum
# to 2020?

def get_three_summands(arr, target):
    # don't allow 0, x, y as a solution
    for i in range(len(arr) - 1, 0, -1):
        try:
            c = arr[i]
            [a, b] = get_two_summands(arr, target - c)
            if(a + b + c == 2020):
                return [a, b, c]
            else:
                raise Exception("There are no three numbers which add up to " + str(target))
        except:
            continue

print("\n2020 - Day 1 - Part 2")
try:
    [a, b, c] = get_three_summands(inputArr, 2020)
    print(a, "*", b, "*", c, "=", a * b * c)
except Exception as e:
    print(str(e))

# => 195 * 511 * 1314 = 130933530
#                       =========