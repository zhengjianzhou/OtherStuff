import itertools as it

def solve24(cs):
    os = set(["".join(i) for i in it.product("+-*/",repeat=3)])
    ns = set(["".join(i) for i in it.permutations(cs)])
    bs = ["(    )         ","(       )      ","   (    )     ","      (    )  ","(    )(    )  ","   (       )  ","             "]
    for oo in os:
        for nn in ns:
            s = "".join(it.chain(*zip(nn,"....",oo+" ")))
            for b in bs:
                sb = "".join(it.chain(*zip(b,s))).replace(" ","").replace("X","10").replace("J","11").replace("Q","12").replace("K","13")
                try:
                    if abs(eval(sb)-24.) < 0.001:
                        print(sb.replace(".","").replace("10","X").replace("11","J").replace("12","Q").replace("13","K"))
                except:
                    pass

solve24("4477")
