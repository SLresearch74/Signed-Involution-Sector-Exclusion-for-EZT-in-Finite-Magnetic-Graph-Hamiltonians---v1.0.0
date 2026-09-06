from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

OUT = Path(__file__).resolve().parent

# Figure 1: oriented-circulant baseline C={1,3}.
n = 8
G = nx.DiGraph()
G.add_nodes_from(range(n))
for j in range(n):
    for c in (1,3):
        G.add_edge(j, (j+c) % n)
pos = nx.circular_layout(G)
fig, ax = plt.subplots(figsize=(5.6,5.6))
nx.draw_networkx_nodes(G, pos, ax=ax, node_size=620)
nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, arrowstyle='-|>', arrowsize=12,
                       width=0.9, connectionstyle='arc3,rad=0.08')
labels = {j: str(j) for j in range(n)}
labels[0] = '0\n$s$'
labels[2] = '2\n$\\ell$'
nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=10)
ax.set_title(r'Oriented-circulant baseline $n=8$, $\mathcal{C}=\{1,3\}$')
ax.set_axis_off()
fig.tight_layout()
fig.savefig(OUT/'n8_baseline_graph.pdf', bbox_inches='tight')
fig.savefig(OUT/'n8_baseline_graph.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 2: affine block/edge generators.
t = np.linspace(-3,3,601)
g = np.abs(t-1)
h = np.abs(t+1)
fig, ax = plt.subplots(figsize=(6.5,4.0))
ax.plot(t, g, label=r'$|g(t)|=|t-1|$')
ax.plot(t, h, label=r'$|h(t)|=|t+1|$')
ax.axvline(1, linestyle='--', linewidth=1)
ax.axvline(-1, linestyle='--', linewidth=1)
ax.annotate('block-dark locus', xy=(1,0), xytext=(1.18,1.0),
            arrowprops=dict(arrowstyle='->'))
ax.annotate('arrow-zero locus', xy=(-1,0), xytext=(-2.85,1.55),
            arrowprops=dict(arrowstyle='->'))
ax.set_xlabel(r'physical parameter $t$')
ax.set_ylabel('absolute generator value')
ax.set_xlim(-3,3)
ax.set_ylim(0,4.2)
ax.legend(frameon=False)
ax.grid(True, linewidth=0.4, alpha=0.35)
fig.tight_layout()
fig.savefig(OUT/'affine_block_edge_loci.pdf', bbox_inches='tight')
fig.savefig(OUT/'affine_block_edge_loci.png', dpi=220, bbox_inches='tight')
plt.close(fig)

# Figure 3: locked family classification. 1=dark block 4, 0=not dark.
events = ['(1,4)','(3,4)','(5,4)','(7,4)','(6,1)','(6,3)','(6,5)','(6,7)']
# forward 0->2, reverse 2->0
M = np.array([
    [0,0],
    [1,1],
    [0,0],
    [1,1],
    [0,1],
    [0,1],
    [0,1],
    [0,1],
], dtype=float)
fig, ax = plt.subplots(figsize=(4.6,5.2))
im = ax.imshow(M, aspect='auto', vmin=0, vmax=1)
ax.set_xticks([0,1], labels=[r'$0\to2$', r'$2\to0$'])
ax.set_yticks(range(len(events)), labels=events)
ax.set_xlabel('marked direction')
ax.set_ylabel(r'event location $(x,y)$')
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        ax.text(j, i, 'dark' if M[i,j] else 'unit', ha='center', va='center', fontsize=9)
ax.set_title('Locked block-4 outcome on $D(t)$')
fig.tight_layout()
fig.savefig(OUT/'locked_n8_block4_map.pdf', bbox_inches='tight')
fig.savefig(OUT/'locked_n8_block4_map.png', dpi=220, bbox_inches='tight')
plt.close(fig)
