import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os
 
# ── НАСТРОЙКИ ──────────────────────────────────────────────
CSV_PATH = "../data/Untitled form.csv"
OUTPUT_DIR = "charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
COLORS = {
    "debate":    "#c9a84c",   # золотой — участники дебатов
    "no_debate": "#4a7eba",   # синий   — не участники
    "bg":        "#0a0e2a",   # фон
    "grid":      "#1a2150",   # сетка
    "text":      "#f5f5f0",   # текст
}
 
# ── ПРАВИЛЬНЫЕ ОТВЕТЫ ───────────────────────────────────────
CORRECT = {
    "q5":  "«Исследования показывают, что 30 минут активности улучшают концентрацию на 20%»",
    "q6":  "Слабый аргумент — один пример не доказывает общую закономерность",
    "q7":  "Статья в рецензируемом научном журнале",
    "q8":  "Успешные люди могут вставать рано по другим причинам, а не потому что это ведёт к успеху",
    "q9":  "Интересно, нужно изучить подробнее и пересмотреть свою позицию",
    "q10": "Признаю, что аргументы сильные, и пересмотрю свою точку зрения",
    "q11": "Определить, какую проблему должна решить форма",
    "q12": "Ошибочный — совпадение по времени не означает причинно-следственную связь",
    "q13": "Составлю список возможных причин и проверю каждую",
}
 
CRITERIA = {
    "Argumentation":       ["q5", "q6"],
    "Source Evaluation":   ["q7", "q8"],
    "Openness to Change":  ["q9", "q10"],
    "Structured Thinking": ["q11", "q12", "q13"],
}
 
# ── ЗАГРУЗКА И ОЧИСТКА ──────────────────────────────────────
df = pd.read_csv(CSV_PATH)
df.columns = [
    "timestamp", "debate_exp", "duration", "format", "grade",
    "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13",
    "self1", "self2", "self3"
]
 
# Очищаем кавычки
for col in ["q5","q6","q7","q8","q9","q10","q11","q12","q13"]:
    df[col] = df[col].str.strip().str.strip('"')
 
# Группы
df["group"] = df["debate_exp"].apply(
    lambda x: "Debate" if "раз" in str(x) or "регулярно" in str(x) else "No Debate"
)
 
debate    = df[df["group"] == "Debate"]
no_debate = df[df["group"] == "No Debate"]
 
print(f"Всего ответов: {len(df)}")
print(f"Участники дебатов: {len(debate)}")
print(f"Не участники: {len(no_debate)}")
 
# ── ПОДСЧЁТ БАЛЛОВ ──────────────────────────────────────────
def score_row(row):
    scores = {}
    for criterion, questions in CRITERIA.items():
        correct = sum(
            1 for q in questions
            if str(row[q]).strip() == CORRECT[q].strip()
        )
        scores[criterion] = (correct / len(questions)) * 100
    return pd.Series(scores)
 
df_scores = df.apply(score_row, axis=1)
df_scores["group"] = df["group"]
 
debate_scores    = df_scores[df_scores["group"] == "Debate"].drop(columns="group")
no_debate_scores = df_scores[df_scores["group"] == "No Debate"].drop(columns="group")
 
debate_means    = debate_scores.mean()
no_debate_means = no_debate_scores.mean()
 
print("\n-- Средние баллы (%) --")
print(f"{'Критерий':<25} {'Дебаты':>10} {'Без дебатов':>12}")
for c in CRITERIA:
    print(f"{c:<25} {debate_means[c]:>9.1f}% {no_debate_means[c]:>11.1f}%")
 
# ── СТИЛЬ ГРАФИКОВ ──────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  COLORS["bg"],
    "axes.facecolor":    COLORS["bg"],
    "axes.edgecolor":    COLORS["grid"],
    "axes.labelcolor":   COLORS["text"],
    "xtick.color":       COLORS["text"],
    "ytick.color":       COLORS["text"],
    "text.color":        COLORS["text"],
    "grid.color":        COLORS["grid"],
    "font.family":       "sans-serif",
})
 
criteria_labels = list(CRITERIA.keys())
 
# ── ГРАФИК 1: Сравнение по критериям (grouped bar) ──────────
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(criteria_labels))
width = 0.35
 
bars1 = ax.bar(x - width/2, [debate_means[c] for c in criteria_labels],
               width, color=COLORS["debate"], alpha=0.9, label="Debate participants")
bars2 = ax.bar(x + width/2, [no_debate_means[c] for c in criteria_labels],
               width, color=COLORS["no_debate"], alpha=0.9, label="Non-participants")
 
ax.set_ylabel("Correct answers (%)", fontsize=11)
ax.set_title("Critical Thinking Scores by Criterion", fontsize=14, fontweight="bold", pad=15)
ax.set_xticks(x)
ax.set_xticklabels(criteria_labels, fontsize=10)
ax.set_ylim(0, 110)
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
ax.legend(fontsize=10)
 
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{bar.get_height():.0f}%", ha="center", va="bottom", fontsize=9, color=COLORS["text"])
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{bar.get_height():.0f}%", ha="center", va="bottom", fontsize=9, color=COLORS["text"])
 
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart1_criteria_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("chart1_criteria_comparison.png saved")
 
# ── ГРАФИК 2: Общий балл — две группы ───────────────────────
df_scores["total"] = df_scores[criteria_labels].mean(axis=1)
 
fig, ax = plt.subplots(figsize=(8, 5))
groups = ["Debate participants", "Non-participants"]
totals = [
    df_scores[df_scores["group"] == "Debate"]["total"].mean(),
    df_scores[df_scores["group"] == "No Debate"]["total"].mean(),
]
colors = [COLORS["debate"], COLORS["no_debate"]]
bars = ax.bar(groups, totals, color=colors, width=0.45, alpha=0.9)
ax.set_ylabel("Overall score (%)", fontsize=11)
ax.set_title("Overall Critical Thinking Score", fontsize=14, fontweight="bold", pad=15)
ax.set_ylim(0, 110)
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
 
for bar, val in zip(bars, totals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f"{val:.1f}%", ha="center", va="bottom", fontsize=12,
            fontweight="bold", color=COLORS["text"])
 
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart2_overall_score.png", dpi=150, bbox_inches="tight")
plt.close()
print("chart2_overall_score.png saved")
 
# ── ГРАФИК 3: Самооценка vs реальный балл ───────────────────
df["self_avg"] = df[["self1","self2","self3"]].apply(pd.to_numeric, errors="coerce").mean(axis=1)
df["total_score"] = df_scores["total"]
 
fig, ax = plt.subplots(figsize=(8, 6))
for grp, color, label in [
    ("Debate",    COLORS["debate"],    "Debate participants"),
    ("No Debate", COLORS["no_debate"], "Non-participants"),
]:
    sub = df[df["group"] == grp]
    ax.scatter(sub["self_avg"], sub["total_score"],
               color=color, alpha=0.7, s=60, label=label)
 
ax.set_xlabel("Self-assessed critical thinking (1–5)", fontsize=11)
ax.set_ylabel("Actual score (%)", fontsize=11)
ax.set_title("Self-Assessment vs Actual Performance", fontsize=14, fontweight="bold", pad=15)
ax.yaxis.grid(True, linestyle="--", alpha=0.4)
ax.xaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
ax.legend(fontsize=10)
 
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart3_self_vs_actual.png", dpi=150, bbox_inches="tight")
plt.close()
print("chart3_self_vs_actual.png saved")
 
# ── ГРАФИК 4: Распределение по опыту дебатов ────────────────
exp_counts = df["debate_exp"].value_counts()
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(exp_counts.index, exp_counts.values,
               color=[COLORS["debate"], COLORS["no_debate"],
                      "#6a9fd8", "#e8c97a"][:len(exp_counts)], alpha=0.9)
ax.set_xlabel("Number of respondents", fontsize=11)
ax.set_title("Respondents by Debate Experience", fontsize=14, fontweight="bold", pad=15)
ax.xaxis.grid(True, linestyle="--", alpha=0.4)
ax.set_axisbelow(True)
 
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            str(int(bar.get_width())), va="center", fontsize=10)
 
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart4_experience_distribution.png", dpi=150, bbox_inches="tight")
plt.close()
print("chart4_experience_distribution.png saved")
 
print("\nВсе графики сохранены в папку charts/")
print("\nИтоговые выводы:")
for c in criteria_labels:
    diff = debate_means[c] - no_debate_means[c]
    print(f"{c}: разница {diff:+.1f}%")
 