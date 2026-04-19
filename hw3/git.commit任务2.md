```python
#任务2  时间分布分析
card_np=data["刷卡类型"].to_numpy()
all=np.sum(card_np==0)
hour_np=data["hour"].to_numpy()
morning=np.sum((hour_np<7) & (card_np==0))
night=np.sum((hour_np>=22) & (card_np==0))
print(morning)
print(night)
morning_pct=morning / all
night_pct=night / all
#绘制柱状图
hour_count=data.groupby("hour").size()
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
colors=["red" if hour<7 else "blue" if hour>=22 else "green" for hour in hour_count.index]
plt.bar(x=hour_count.index,height=hour_count.values,color=colors)
plt.title("24小时刷卡量分布柱状图")
plt.xlabel("小时")
plt.ylabel("刷卡量")
plt.xticks(np.arange(0, 24, 2))
plt.grid(axis='y', linestyle='--', alpha=0.7)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='red', label='早间(<7点)'),
    Patch(facecolor='green', label='白天(7-22点)'),
    Patch(facecolor='blue', label='夜间(≥22点)')
]
plt.legend(handles=legend_elements, loc="upper right", fontsize=11)
plt.tight_layout()
save_path=os.path.join(folder,"hour_distribution.png")
plt.savefig(save_path,dpi=150)
plt.show()
```

