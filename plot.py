import matplotlib.pyplot as plt
import seaborn as sns
import pandas

fig_path = "/mnt/d/work/code_projects/complete/tsw_script/data/results/tsw_anom_Paraná.csv"

data = pandas.read_csv(fig_path)

plt.figure(figsize=(7,7))

ax = sns.lineplot(x='date',
             y='tsw_anomaly(cm)',            
             data=data )

ax.set(ylim=(-100,100))

plt.show()

