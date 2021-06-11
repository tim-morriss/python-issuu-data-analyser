import os
from graphviz import Digraph

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin/'


class LikesGraph:

    @staticmethod
    def draw_likes_graph(user_id, doc_id, data_analyser):
        da = data_analyser

        # get the top 'also liked' docs
        top = da.top_also_like(doc_id, 10, user_id)

        # get the readers of all the 'also likes' documents
        readers = da.likes
        lines = data_analyser.json_loader.lines
        # adapted from https://stackoverflow.com/a/45846841
        num = float('{:.3g}'.format(lines))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        size = '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

        dot = Digraph(name='Also likes')

        # create labels
        dot.node('Readers', shape='none')
        dot.node('Documents', shape='none')
        dot.edge('Readers', 'Documents', label="Size: %s" % size)

        try:
            # print(user_id)
            if user_id:
                dot.node(user_id[-4:], style='filled', fillcolor='green', shape='box')
                dot.node(doc_id[-4:], style='filled', fillcolor='green', shape='circle')
                dot.edge(user_id[-4:], doc_id[-4:])
            else:
                dot.node(doc_id[-4:], style='filled', fillcolor='green', shape='circle')

            # go through each reader and make a node for them
            for reader in readers:
                # if the reader is the one supplied as user_id, skip them
                if reader == user_id:
                    continue
                else:
                    dot.node(reader[-4:], shape='box')
                for doc in readers[reader]:
                    # for each reader in readers check the documents they have read
                    if doc in top:
                        dot.node(doc[-4:], shape='circle')
                        dot.edge(reader[-4:], doc[-4:])

            dot.render('./graphs/' + user_id + '_' + doc_id, view=True)
        except TypeError:
            # catch TypeError when there is nothing to plot
            print("There is nothing to plot!")
