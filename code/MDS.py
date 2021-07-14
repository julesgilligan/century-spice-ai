from typing import Callable
from sklearn.manifold import MDS
import numpy as np
from numpy import mean
import matplotlib.pyplot as plt
import mplcursors
from package.structures import MCs_from_file, MerchantCard
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation

class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

def calc_synergy(c1, c2):
    way_one = 15
    good = -4
    bad = 1
    for cube in c1.cost:
        if cube in c2.reward:
            way_one += good
        if cube in c2.cost:
            way_one += bad
    way_two = 15
    for cube in c2.cost:
        if cube in c1.reward:
            way_two += good
        if cube in c1.cost:
            way_two += bad
    return mean([way_one, way_two])

def calc_synergy_pile(c1, c2):
    pile = [cube for cube in c1.cost]
    for cube in c2.cost:
        pile.append(cube)
    big_size = max(len(pile), 1)
    for cube in [c1.reward, c2.reward]:
        try:
            pile.remove(cube)
        finally:
            continue
    return len(pile) / big_size

def generate_distances(func : Callable[[MerchantCard, MerchantCard],float]):
    with open('./package/MerchantCards.txt') as f: 
        MCs = MCs_from_file(f)
    card_count = len(MCs)
    X = np.zeros((card_count,card_count))
    for i in range(card_count):
        for j in range(i + 1, card_count):
            X[i][j] = func(MCs[i], MCs[j])
            X[j][i] = X[i][j]
    return X, MCs

def graph_MDS(X,MCs):
    fig = plt.figure(figsize=(10,5))

    # Figure 1: 3D
    thax = fig.add_subplot(1,2,1,projection='3d')
    model = MDS(n_components=3, dissimilarity='precomputed', random_state=1)
    out = model.fit_transform(X)
    thax.scatter(out[:, 0], out[:, 1], out[:, 2])

    for i, xyz_ in enumerate(out):
        label = "".join( (str(x) for x in MCs[i].cost) ) + "," + "".join( (str(x) for x in MCs[i].reward) )
        tag = Annotation3D(label, xyz=xyz_, fontsize=10, xytext=(-3,3),
                textcoords='offset points', ha='right',va='bottom')
        thax.add_artist(tag)

    # Figure 2: 2D
    ax = fig.add_subplot(1,2,2)
    model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
    out = model.fit_transform(X)
    ax.scatter(out[:, 0], out[:, 1])
    mplcursors.cursor(ax).connect( "add", 
        lambda sel: 
            sel.annotation.set_text(f"{MCs[sel.target.index].cost},{MCs[sel.target.index].reward}") )

    plt.axis('equal')

    plt.show()

distances, merchant_cards = generate_distances(func=calc_synergy)
graph_MDS(distances,merchant_cards)
