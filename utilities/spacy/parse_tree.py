import sys;

def show_tree_for_sentence(sent):
    def __showTree(token, level):
        tab = "\t" * level
        sys.stdout.write("\n%s{" % (tab))
        [__showTree(t, level+1) for t in token.lefts]
        sys.stdout.write("\n%s\t%s [%s] (%s) (%s) (@%s)" % (tab,token,token.dep_,token.tag_, token.pos_, str(token.i)))
        [__showTree(t, level+1) for t in token.rights]
        sys.stdout.write("\n%s}" % (tab))
    return __showTree(sent.root, 1)